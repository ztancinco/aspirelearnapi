"""
View for listing and creating lessons.

This file contains the view class for handling lesson listing and creation.
"""

from typing import Optional, Dict, Any, List
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from ...services.lesson_service import LessonService
from ..serializers.lesson_serializer import LessonSerializer


class LessonsView(APIView):
    """
    View for listing, creating, updating, and deleting lessons.
    """

    def __init__(self, **kwargs: Any) -> None:
        """
        Constructor to inject LessonService into the view.
        """
        super().__init__(**kwargs)
        self.lesson_service: LessonService = LessonService()

    @extend_schema(
        responses={200: LessonSerializer(many=True)},
        parameters=[
            OpenApiParameter(
                name="lesson_id",
                type="integer",
                required=False,
                description="Lesson ID",
            )
        ],
    )
    def get(
        self,
        _request: Request,
        course_id: Optional[int] = None,
        lesson_id: Optional[int] = None,
    ) -> Response:
        """
        Retrieve all lessons or a single lesson by ID, optionally filtered by course_id.
        """
        if lesson_id:
            lesson: Dict[str, Any] = self.lesson_service.get_lesson_by_id(lesson_id)
            return Response(lesson, status=status.HTTP_200_OK)

        if course_id:
            lessons: List[Dict[str, Any]] = (
                self.lesson_service.get_lessons_by_course_id(course_id)
            )
            return Response(lessons, status=status.HTTP_200_OK)

        lessons: List[Dict[str, Any]] = self.lesson_service.get_all_lessons()
        return Response(lessons, status=status.HTTP_200_OK)

    @extend_schema(request=LessonSerializer, responses={201: LessonSerializer})
    def post(self, request: Request, course_id: int) -> Response:
        """
        Create a new lesson for the given course_id.
        """
        lesson_data: Dict[str, Any] = request.data
        lesson_data["course_id"] = course_id
        lesson: Dict[str, Any] = self.lesson_service.create_lesson(lesson_data)
        return Response(lesson, status=status.HTTP_201_CREATED)

    @extend_schema(request=LessonSerializer, responses={200: LessonSerializer})
    def put(self, request: Request, lesson_id: int) -> Response:
        """
        Update an existing lesson.
        """
        lesson: Dict[str, Any] = self.lesson_service.update_lesson(
            lesson_id, request.data
        )
        return Response(lesson, status=status.HTTP_200_OK)

    @extend_schema(
        responses={
            204: OpenApiParameter(
                name="message", type="string", description="Lesson deleted successfully"
            )
        }
    )
    def delete(self, _request: Request, lesson_id: int) -> Response:
        """
        Delete a lesson by ID.
        """
        self.lesson_service.delete_lesson(lesson_id)
        return Response(
            {"message": "Lesson deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
