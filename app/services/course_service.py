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

    def get_all_courses(self) -> List[Dict[str, Any]]:
        """
        Retrieve all courses and serialize them.

        :return: List of serialized course data.
        """
        courses = CourseModel.objects.all()  # pylint: disable=no-member
        serializer: CourseSerializer = CourseSerializer(courses, many=True)
        return serializer.data

    def get_course_by_id(self, course_id: int) -> Dict[str, Any]:
        """
        Retrieve a course by its ID and serialize it.

        :param course_id: ID of the course to retrieve.
        :return: Serialized course data as a dictionary.
        """
        course: CourseModel = get_object_or_404(CourseModel, id=course_id)
        serializer: CourseSerializer = CourseSerializer(course)
        return serializer.data

    def create_lessons_and_quizzes(self,
         course: CourseModel,
         lessons: List[Dict[str, Any]],
         quizzes: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Create associated lessons and quizzes for a course.
        """
        for lesson in lessons:
            if not course.id:
                raise ValueError('Course ID is missing for the lesson.')
            lesson['course'] = course.id
            self.lesson_service.create_lesson(lesson_data=lesson)

        for quiz in quizzes:
            if not course.id:
                raise ValueError('Course ID is missing for the lesson.')
            if not quiz.get('questions'):
                raise ValueError('Each quiz must have questions.')

            quiz['course'] = course.id
            created_quiz: Dict[str, Any] = self.quiz_service.create_quiz(quiz)

            for question_data in quiz['questions']:
                self.question_service.create_question(created_quiz['id'], question_data)

    def create_course(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new course along with associated lessons and quizzes.

        :param data: Dictionary containing course data.
        :return: Serialized course data.
        :raises ValueError: If a quiz is missing questions.
        """
        if 'instructor' not in data:
            raise ValueError("Instructor is required")

        serializer: CourseSerializer = CourseSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        course = serializer.save()

        self.create_lessons_and_quizzes(course, data.get('lessons', []), data.get('quizzes', []))

        return CourseSerializer(course).data

    def update_course(self, course_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing course.

        :param course_id: ID of the course to update.
        :param data: Dictionary containing updated course data.
        :return: Serialized updated course data.
        """
        course: CourseModel = get_object_or_404(CourseModel, id=course_id)
        serializer: CourseSerializer = CourseSerializer(course, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def delete_course(self, course_id: int) -> None:
        """
        Delete a course by its ID.

        :param course_id: ID of the course to delete.
        """
        course: CourseModel = get_object_or_404(CourseModel, id=course_id)
        course.delete()
