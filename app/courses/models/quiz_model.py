"""
This file contains the quiz model.
"""

from django.db import models
from .course_model import CourseModel
from ...abstract.soft_delete_model import SoftDeleteModel

class QuizModel(SoftDeleteModel):
    """
    Model representing a quiz.
    """
    title = models.CharField(max_length=255)
    course = models.ForeignKey(CourseModel, on_delete=models.CASCADE, related_name='quizzes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        """
        Meta options for QuizModel.
        """
        db_table = 'quizzes'
        indexes = [
            models.Index(fields=['deleted_at']),
        ]
