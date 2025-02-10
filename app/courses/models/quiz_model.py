"""
This file contains the quiz model.
"""

from django.db import models
from .course_model import CourseModel


class QuizModel(models.Model):
    """
    Model representing a quiz.
    """

    title = models.CharField(max_length=255)
    course = models.ForeignKey(
        CourseModel, on_delete=models.CASCADE, related_name="quizzes"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta options for QuizModel.
        """

        db_table = "quizzes"
