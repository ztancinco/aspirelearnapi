"""
Serializer for Courses.
"""

from rest_framework import serializers
from ..models.course_model import CourseModel
from .lesson_serializer import LessonsSerializer

class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for the CourseModel.
    """
    lessons = LessonsSerializer(many=True, read_only=True)

    class Meta:
        """
        Meta class for CourseSerializer.
        """
        model = CourseModel
        fields = ['id', 'title', 'description', 'instructor', 'created_at', 'lessons']
