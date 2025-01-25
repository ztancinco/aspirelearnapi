"""
Serializer for Question.
"""

from rest_framework import serializers
from ..models.question_model import QuestionModel
from .answer_serializer import AnswerSerializer

class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer class for QuestionModel.
    """
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        """
        Meta class to define the model and fields for the QuestionSerializer.
        """
        model = QuestionModel
        fields = ['id', 'text', 'answers']

    def __str__(self):
        """
        String representation of the QuestionSerializer instance.

        Returns a string with the question's ID and text.
        """
        return f"Question({self.instance.id}, {self.instance.text})"
