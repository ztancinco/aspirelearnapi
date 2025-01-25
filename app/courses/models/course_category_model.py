"""
This is the model for the category of the course in the application.
"""

from django.db import models
from ...abstract.soft_delete_model import SoftDeleteModel

class CourseCategoryModel(SoftDeleteModel):
    """
    A model representing a category of the course in the application.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.name) if self.name else "No Category Name"

    class Meta:
        """
        Meta options for CourseCategoryModel.
        """
        db_table = 'course_categories'
        indexes = [
            models.Index(fields=['deleted_at']),
        ]
