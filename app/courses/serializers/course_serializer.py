"""
Serializer for Courses.
"""

from typing import Dict, Any
from rest_framework import serializers
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from ..models.course_model import CourseModel
from .lesson_serializer import LessonSerializer
from .quiz_serializer import QuizSerializer
from ..serializers.users.instructor_serializer import InstructorSerializer

User = get_user_model()


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for the CourseModel.
    """

    lessons = LessonSerializer(many=True, read_only=True)
    quizzes = QuizSerializer(many=True, read_only=True)
    instructor = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        """
        Meta class for CourseSerializer.
        """

        model = CourseModel
        fields = [
            "id",
            "title",
            "description",
            "instructor",
            "created_at",
            "lessons",
            "quizzes",
        ]

    def validate_title(self, value):
        """
        Ensure that a course with the same title does not exist unless it's deleted,
        and allow updates to the course itself (ignore the course being updated).
        """
        course_instance = getattr(self, "instance", None)

        # Check if this is an update, and if so, ignore the current course instance
        if course_instance:
            existing_course = CourseModel.objects.filter(
                title=value, deleted_at__isnull=True
            ).exclude(
                id=course_instance.id
            )  # Exclude the current course instance
        else:
            # If it's a new course, no need to exclude anything
            existing_course = CourseModel.objects.filter(
                title=value, deleted_at__isnull=True
            )

        # If another course with the same title exists and is not deleted, raise an error
        if existing_course.exists():
            raise serializers.ValidationError(
                "A course with this title already exists."
            )

        return value

    @extend_schema(
        responses={200: InstructorSerializer()},
    )
    def to_representation(self, instance: CourseModel) -> Dict[str, Any]:
        """
        Customize the output representation to use InstructorSerializer for the instructor field.

        Args:
            instance: The CourseModel instance to be serialized.

        Returns:
            A dictionary representation of the serialized course instance.
        """
        representation = super().to_representation(instance)
        serialized_data = InstructorSerializer(instance.instructor).data
        representation["instructor"] = serialized_data

        lessons = representation.get("lessons", [])
        sorted_lessons = sorted(lessons, key=lambda x: x["order"])
        representation["lessons"] = sorted_lessons
        return representation
