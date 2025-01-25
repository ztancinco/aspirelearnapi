"""
Module defining the LessonsModel for courses.
"""

from django.db import models
from .course_model import CourseModel
from ...abstract.soft_delete_model import SoftDeleteModel

class LessonsModel(SoftDeleteModel):
    """
    Model representing a lesson in a course.
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    course = models.ForeignKey(
        CourseModel,
        on_delete=models.CASCADE,
        related_name='lessons'
    )
    video_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """
        String representation of a LessonsModel instance.
        """
        return f"Course: {self.course.title} - {self.order}. {self.title}"  # pylint: disable=no-member

    class Meta:
        """
        Meta options for LessonsModel.
        
        - Ensures indexing on `deleted_at` for optimized querying.
        """
        db_table = 'lessons'
        indexes = [
            models.Index(fields=['deleted_at']),
        ]
