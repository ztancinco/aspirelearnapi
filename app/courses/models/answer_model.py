"""
Model for Answer.
"""

from django.db import models
from .question_model import QuestionModel


class AnswerModel(models.Model):
    """
    Model representing an answer to a quiz question.
    """

    question = models.ForeignKey(
        QuestionModel, on_delete=models.CASCADE, related_name="answers"
    )  # pylint: disable=no-member
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    is_multiple_choice = models.BooleanField(default=False)

    class Meta:
        """
        Meta options for AnswerModel.
        """

        db_table = "answers"

    def __str__(self):
        return (
            f"Answer to {self.question.pk}: {self.text} "  # pylint: disable=no-member
            f"({'Correct' if self.is_correct else 'Incorrect'})"
        )
