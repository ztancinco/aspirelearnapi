"""
This is the model for the Question in the application.
"""
from django.db import models
from .quiz_model import QuizModel
from ...abstract.soft_delete_model import SoftDeleteModel

class QuestionModel(SoftDeleteModel):
    """
    A model representing a question related to the Quiz in the application.
    """
    quiz = models.ForeignKey(QuizModel, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.text) if self.text else "No Question"

    class Meta:
        """
        Meta options for QuestionModel.
        """
        db_table = 'questions'
        indexes = [
            models.Index(fields=['deleted_at']),
        ]
        