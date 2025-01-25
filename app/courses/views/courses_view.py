"""
View for listing, creating, and deleting courses.

This file contains the view class for handling courses.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...services.course_service import CourseService

class CoursesView(APIView):
    """
    View for managing courses using CoursesService.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize CoursesService as an instance variable.
        """
        super().__init__(*args, **kwargs)
        self.course_service = CourseService()

    def get(self, _, course_id=None):
        """
        Retrieve all courses or a single course by ID.
        """
        if course_id:
            course = self.course_service.get_course_by_id(course_id)
            return Response(course, status=status.HTTP_200_OK)

        courses = self.course_service.get_all_courses()
        return Response(courses, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new course.
        """
        course = self.course_service.create_course(request.data)
        return Response(course, status=status.HTTP_201_CREATED)

    def put(self, request, course_id):
        """
        Update an existing course.
        """
        course = self.course_service.update_course(course_id, request.data)
        return Response(course, status=status.HTTP_200_OK)

    def delete(self, _, course_id):
        """
        Delete a course by ID.
        """
        self.course_service.delete_course(course_id)
        return Response(
            {"message": "Course deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
