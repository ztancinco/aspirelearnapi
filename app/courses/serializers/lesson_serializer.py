"""
Serializer for Lessson.
"""

from rest_framework import serializers
from ..models.lesson_model import LessonsModel

class LessonsSerializer(serializers.ModelSerializer):
    """
    Serializer for the LessonsModel.

    This serializer converts LessonsModel instances into JSON format 
    and validates incoming data for lesson-related API operations.
    """

    class Meta:
        """
        Meta class to define the model and fields for serialization.

        Specifies the model being serialized (LessonsModel) and the 
        fields to include in the serialized output.
        """
        model = LessonsModel
        fields = ['id', 'title', 'content', 'video_url', 'order']
