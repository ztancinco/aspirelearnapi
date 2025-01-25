"""
Service for managing courses.

This is a service class to handle actions related to courses.
"""

from django.shortcuts import get_object_or_404
from ..courses.models.course_model import CourseModel
from ..courses.serializers.course_serializer import CourseSerializer
from ..services.quiz_service import QuizService
from ..services.question_service import QuestionService

class CourseService:
    """
    Service class for handling course-related operations.
    """
    def __init__(self):
        """
        Initialize the service with an instance of the CourseModel.
        """
        self.course_model = CourseModel
        self.quiz_service = QuizService()
        self.question_service = QuestionService()

    def get_all_courses(self):
        """
        Retrieve all courses and serialize them.
        """
        courses = CourseModel.objects.all()  # pylint: disable=no-member
        serializer = CourseSerializer(courses, many=True)
        return serializer.data

    def get_course_by_id(self, course_id):
        """
        Retrieve a course by its ID and serialize it.

        :param course_id: ID of the course to retrieve
        :return: Serialized course data
        """
        course = get_object_or_404(CourseModel, id=course_id)
        serializer = CourseSerializer(course)
        return serializer.data

    def create_course(self, data):
        """
        Create a new course and associated quizzes and questions.

        :param data: Dictionary containing course data
        :return: Serialized course data
        """
        # Validate and save the course
        serializer = CourseSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Handle quizzes
        quizzes = data.get('quizzes', [])
        for quiz_data in quizzes:
            if not quiz_data.get('questions'):
                raise ValueError('Each quiz must have questions.')

            # Add course_id to quiz data and create the quiz
            quiz_data['course_id'] = serializer.data['id']
            created_quiz = self.quiz_service.create_quiz(quiz_data)

            # Create questions for the quiz
            for question_data in quiz_data['questions']:
                self.question_service.create_question(created_quiz['id'], question_data)

        return serializer.data

    def update_course(self, course_id, data):
        """
        Update an existing course.

        :param course_id: ID of the course to update
        :param data: Dictionary containing updated course data
        :return: Serialized updated course data
        """
        course = get_object_or_404(CourseModel, id=course_id)
        serializer = CourseSerializer(course, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def delete_course(self, course_id):
        """
        Delete a course by its ID.

        :param course_id: ID of the course to delete
        """
        course = get_object_or_404(CourseModel, id=course_id)
        course.delete()
