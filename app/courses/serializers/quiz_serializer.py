"""
Serializers for Quiz.
"""

from rest_framework import serializers
from ..models.quiz_model import QuizModel
from .question_serializer import QuestionSerializer

class QuizSerializer(serializers.ModelSerializer):
    """
    Serializer class for QuizModel.
    """
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        """
        Meta class to define the model and fields for the QuizSerializer.
        """
        model = QuizModel
        fields = ['id', 'title', 'course', 'questions']

    def __str__(self):
        """
        String representation of the QuizSerializer instance.

        Returns a string with the quiz's ID and title.
        """
        return f"Quiz({self.instance.id}, {self.instance.title})"
