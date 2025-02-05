"""
View for listing, creating, and deleting courses.

This file contains the view class for handling courses.
"""
from typing import Optional, Any
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from ...services.course_service import CourseService

class CoursesView(APIView):
    """
    View for managing courses using CoursesService.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize CoursesService as an instance variable.
        """
        super().__init__(*args, **kwargs)
        self.course_service: CourseService = CourseService()

    def get(self, _request: Request, course_id: Optional[int] = None) -> Response:
        """
        Retrieve all courses or a single course by ID.
        """
        if course_id:
            course = self.course_service.get_course_by_id(course_id)
            return Response(course, status=status.HTTP_200_OK)

        courses = self.course_service.get_all_courses()
        return Response(courses, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        """
        Create a new course.
        """
        course = self.course_service.create_course(request.data)
        return Response(course, status=status.HTTP_201_CREATED)

    def put(self, request: Request, course_id: int) -> Response:
        """
        Update an existing course.
        """
        course = self.course_service.update_course(course_id, request.data)
        return Response(course, status=status.HTTP_200_OK)

    def delete(self, _request: Request, course_id: int) -> Response:
        """
        Delete a course by ID.
        """
        self.course_service.delete_course(course_id)
        return Response(
            {"message": "Course deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
