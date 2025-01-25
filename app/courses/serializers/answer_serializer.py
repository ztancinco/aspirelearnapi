"""
Serializer for Answer.
"""

from rest_framework import serializers
from ..models.answer_model import AnswerModel

class AnswerSerializer(serializers.ModelSerializer):
    """
    Serializer class for AnswerModel.
    """
    class Meta:
        """
        Meta class to define the model and fields for the AnswerSerializer.
        """
        model = AnswerModel
        fields = ['id', 'text', 'is_correct']

    def __str__(self):
        """
        String representation of the AnswerSerializer instance.
        """
        if self.instance:
            return f"Answer({self.instance.id}, {self.instance.text})"
        return "Answer(unsaved instance)"
