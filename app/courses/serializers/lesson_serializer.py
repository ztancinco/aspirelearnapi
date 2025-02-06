"""
Serializer for Lessson.
"""

from rest_framework import serializers
from ..models.lesson_model import LessonModel

class LessonSerializer(serializers.ModelSerializer):
    """
    Serializer for the LessonModel.

    This serializer converts LessonModel instances into JSON format 
    and validates incoming data for lesson-related API operations.
    """

    class Meta:
        """
        Meta class to define the model and fields for serialization.

        Specifies the model being serialized (LessonModel) and the 
        fields to include in the serialized output.
        """
        model = LessonModel
        fields = ['id', 'title', 'content', 'video_url', 'order','course']
