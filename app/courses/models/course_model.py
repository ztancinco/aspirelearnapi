"""
This is the model for the course in the application.
"""

from django.db import models
from django.contrib.auth import get_user_model
from ...abstract.soft_delete_model import SoftDeleteModel
from .course_category_model import CourseCategoryModel

User = get_user_model()

class CourseModel(SoftDeleteModel):
    """
    A model representing a course in the application.
    """
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    category = models.ForeignKey(CourseCategoryModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.title) if self.title else "Untitled Course"

    class Meta:
        """
        Meta options for CourseModel.
        """
        db_table = 'courses'
        indexes = [
            models.Index(fields=['deleted_at']),
        ]
