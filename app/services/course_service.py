"""
Service for managing courses.

This is a service class to handle actions related to courses.
"""

from typing import Any, Dict, List
from django.shortcuts import get_object_or_404
from ..courses.models.course_model import CourseModel
from ..courses.serializers.course_serializer import CourseSerializer
from ..services.lesson_service import LessonService
from ..services.quiz_service import QuizService
from ..services.question_service import QuestionService
from ..services.answer_service import AnswerService
from ..services.logger_service import LoggerService


class CourseService:
    """
    Service class for handling course-related operations.
    """

    def __init__(self) -> None:
        """
        Initialize the service with instances of related services.
        """
        self.course_model: CourseModel = CourseModel
        self.quiz_service: QuizService = QuizService()
        self.lesson_service: LessonService = LessonService()
        self.question_service: QuestionService = QuestionService()
        self.answer_service: AnswerService = AnswerService()
        self.logger_service: LoggerService = LoggerService(__name__)

    def get_all_courses(self) -> List[Dict[str, Any]]:
        """
        Retrieve all courses and serialize them.

        :return: List of serialized course data.
        """
        courses = CourseModel.objects.all()  # pylint: disable=no-member
        return CourseSerializer(courses, many=True).data

    def get_course_by_id(self, course_id: int) -> Dict[str, Any]:
        """
        Retrieve a course by its ID and serialize it.

        :param course_id: ID of the course to retrieve.
        :return: Serialized course data as a dictionary.
        """
        course: CourseModel = get_object_or_404(CourseModel, id=course_id)
        return CourseSerializer(course).data

    def create_lessons_and_quizzes(
        self,
        course: CourseModel,
        lessons: List[Dict[str, Any]],
        quizzes: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Create associated lessons and quizzes for a course.
        """
        for lesson in lessons:
            if not course.id:
                raise ValueError("Course ID is missing for the lesson.")

            lesson["course"] = course.id
            created_lesson = self.lesson_service.create_lesson(lesson_data=lesson)
            if not created_lesson.get("id"):
                raise ValueError(
                    f"Failed to Lesson: {lesson.get('title', 'Unknown title')}."
                )

        if len(quizzes) > 0:
            for quiz in quizzes:
                if not course.id:
                    raise ValueError("Course ID is missing for the quiz.")
                if not quiz.get("questions"):
                    raise ValueError("Each quiz must have questions.")
                if not quiz.get("title"):
                    raise ValueError("Quiz title/text is missing.")
                quiz["course"] = course.id

                created_quiz = self.quiz_service.create_quiz(quiz)
                if created_quiz.get("id") is None:
                    raise ValueError(
                        f"Failed to create quiz: {quiz.get('title', 'Unknown title')}."
                    )

                question_ctr = 1
                for question_data in quiz["questions"]:
                    question = question_data.get("title")
                    if not question:
                        raise ValueError(
                            "Question " + str(question_ctr) + " is missing."
                        )
                    del question_data["title"]
                    question_data["text"] = question
                    question_data["quiz"] = created_quiz.get("id")
                    self.logger_service.debug(
                        f"Processing question data: {question_data}"
                    )
                    created_question = self.question_service.create_question(
                        created_quiz.get("id"), question_data
                    )

                    self._create_or_update_answers(
                        created_question["id"], question_data
                    )
                question_ctr += 1

    def update_lessons_and_quizzes(
        self,
        course: CourseModel,
        lessons: List[Dict[str, Any]],
        quizzes: List[Dict[str, Any]],
    ) -> None:
        """
        Update lessons and quizzes for a given course.

        :param course: The CourseModel instance to update.
        :param lessons: List of lesson data to update or create.
        :param quizzes: List of quiz data to update or create.
        """
        existing_lessons = {lesson.id: lesson for lesson in course.lessons.all()}
        existing_quizzes = {quiz.id: quiz for quiz in course.quizzes.all()}

        # Update or create lessons
        for lesson in lessons:
            lesson_id = lesson.get("id")
            if lesson_id and lesson_id in existing_lessons:
                self.lesson_service.update_lesson(lesson_id, lesson)
            else:
                lesson["course"] = course.id
                self.lesson_service.create_lesson(lesson)

        # Update or create quizzes and associated questions and answers
        for quiz in quizzes:
            quiz_id = quiz.get("id")
            if quiz_id and quiz_id in existing_quizzes:
                self.quiz_service.update_quiz(quiz_id, quiz)
            else:
                quiz["course"] = course.id
                created_quiz = self.quiz_service.create_quiz(quiz)

                for question_data in quiz.get("questions", []):
                    self._create_or_update_question_and_answers(
                        created_quiz["id"], question_data
                    )

    def _create_or_update_question_and_answers(
        self, quiz_id: int, question_data: Dict[str, Any]
    ) -> None:
        """
        Create or update a question and its answers for a given quiz.

        :param quiz_id: The ID of the quiz where the question belongs.
        :param question_data: The data for the question, including options and correct answer.
        """
        # Create or update the question
        question_text = question_data.get("title")
        if not question_text:
            raise ValueError("Question title is missing.")

        question_data["text"] = question_text
        created_question = self.question_service.create_question(quiz_id, question_data)

        # Create or update the answers for the question
        self._create_or_update_answers(created_question["id"], question_data)

    def _create_or_update_answers(
        self, question_id: int, question_data: Dict[str, Any]
    ) -> None:
        """
        Create or update answers for a given question.

        :param question_id: ID of the question for which to update or create answers.
        :param question_data: Data containing the options and correct answer.
        """
        existing_answers = {
            answer.text: answer
            for answer in self.answer_service.get_answers_by_question(question_id)
        }

        # Handle answers based on whether it's a multiple-choice question
        if question_data.get("is_multiple_choice"):
            options_data = question_data.get("options", [])
            correct_answer = question_data.get("correct_answer")

            # Delete answers that no longer exist
            for option in existing_answers.keys():
                if option not in options_data:
                    self.answer_service.delete_answer_by_question_and_text(
                        question_id, option
                    )

            # Add new answers or update existing ones
            for option in options_data:
                is_correct = option == correct_answer
                if option not in existing_answers:
                    self.answer_service.create_answer(
                        question_id,
                        {
                            "text": option,
                            "is_correct": is_correct,
                            "is_multiple_choice": True,
                        },
                    )
                else:
                    answer = existing_answers[option]
                    if answer.is_correct != is_correct:
                        answer.is_correct = is_correct
                        answer.save()

        else:
            # For non-multiple-choice questions, handle the single answer
            correct_answer = question_data.get("correct_answer")
            existing_answer = existing_answers.get(correct_answer)

            if existing_answer:
                # Update if necessary
                existing_answer.is_correct = True
                existing_answer.save()
            else:
                # Create a new answer
                self.answer_service.create_answer(
                    question_id,
                    {
                        "text": correct_answer,
                        "is_correct": True,
                        "is_multiple_choice": False,
                    },
                )

    def create_course(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new course along with associated lessons and quizzes.

        :param data: Dictionary containing course data.
        :return: Serialized course data.
        :raises ValueError: If a quiz is missing questions.
        """
        if "instructor" not in data:
            raise ValueError("Instructor is required")

        serializer: CourseSerializer = CourseSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        course = serializer.save()

        self.create_lessons_and_quizzes(
            course, data.get("lessons", []), data.get("quizzes", [])
        )

        return CourseSerializer(course).data

    def update_course(self, course_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing course along with its lessons and quizzes.

        :param course_id: ID of the course to update.
        :param data: Dictionary containing updated course data.
        :return: Serialized updated course data.
        """
        course: CourseModel = get_object_or_404(CourseModel, id=course_id)

        # Update the course data
        serializer: CourseSerializer = CourseSerializer(course, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Update lessons and quizzes if provided
        lessons = data.get("lessons", [])
        quizzes = data.get("quizzes", [])
        if lessons or quizzes:
            self.update_lessons_and_quizzes(course, lessons, quizzes)

        return serializer.data

    def delete_course(self, course_id: int) -> None:
        """
        Delete a course by its ID.

        :param course_id: ID of the course to delete.
        """
        course: CourseModel = get_object_or_404(CourseModel, id=course_id)
        course.delete()
