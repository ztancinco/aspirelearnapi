"""
This module contains abstract models and base classes used throughout the app.
"""

from django.db import models
from django.utils import timezone

class SoftDeleteModel(models.Model):
    """
    An abstract model providing soft deletion functionality.
    
    This model includes common fields for soft deletion, such as `created_at`, `updated_at`,
    and `deleted_at`. It also provides a custom `delete` method that performs a soft delete
    by setting the `deleted_at` timestamp instead of actually removing the record.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self, using=None, keep_parents=False):
        """
        Perform a soft delete by setting the `deleted_at` timestamp.
        """
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        """
        Provide a string representation of the model.
        """
        return str(self.name) if hasattr(self, 'name') else "Unnamed"

    class Meta:
        """
        Meta options for SoftDeleteModel.
        """
        abstract = True
        indexes = [
            models.Index(fields=['deleted_at']),
        ]
