"""
Service for managing lessons.

This is a service class to handle actions related to lessons.
"""

from typing import Dict, Any
from django.shortcuts import get_object_or_404
from ..courses.models.lesson_model import LessonModel
from ..courses.serializers.lesson_serializer import LessonSerializer
from .utils import handle_video_upload


class LessonService:
    """
    Service class for handling lesson-related operations.
    """

    def create_lesson(self, lesson_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new lesson.

        :param lesson_data: Data for the lesson.
        :return: Serialized lesson data.
        """
        video_file = lesson_data.get("video", None)
        lesson_data["video_url"] = handle_video_upload(video_file) if video_file else ""
        lesson_serializer = LessonSerializer(data=lesson_data)
        lesson_serializer.is_valid(raise_exception=True)
        lesson_serializer.save()
        return lesson_serializer.data

    def get_lesson_by_id(self, lesson_id: int) -> Dict[str, Any]:
        """
        Retrieve a lesson by its ID.

        :param lesson_id: ID of the lesson to retrieve.
        :return: Serialized lesson data.
        """
        lesson = get_object_or_404(LessonModel, id=lesson_id)
        serializer = LessonSerializer(lesson)
        return serializer.data

    def update_lesson(
        self, lesson_id: int, lesson_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update an existing lesson.

        :param lesson_id: ID of the lesson to update.
        :param lesson_data: Data for the lesson update.
        :return: Serialized updated lesson data.
        """
        lesson = get_object_or_404(LessonModel, id=lesson_id)
        video_file = lesson_data.get("video", None)
        lesson_data["video_url"] = handle_video_upload(video_file) if video_file else ""
        lesson_serializer = LessonSerializer(lesson, data=lesson_data, partial=True)
        lesson_serializer.is_valid(raise_exception=True)
        lesson_serializer.save()
        return lesson_serializer.data

    def delete_lesson(self, lesson_id: int) -> None:
        """
        Delete a lesson by its ID.

        :param lesson_id: ID of the lesson to delete.
        """
        lesson = get_object_or_404(LessonModel, id=lesson_id)
        lesson.delete()

    def get_all_lessons(self) -> Dict[str, Any]:
        """
        Retrieve all lessons and serialize them.

        :return: List of serialized lesson data.
        """
        lessons = LessonModel.objects.all()  # pylint: disable=no-member
        serializer = LessonSerializer(lessons, many=True)
        return serializer.data
