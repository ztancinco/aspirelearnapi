"""
This contains the custom user model for the Dash application.

Models:
    - DashUserModel: Custom user model with email as the primary identifier, 
      user roles, biography, and timestamps for creation, update, and soft deletion.
    - DashUserGroups: Intermediate model for the ManyToMany relationship 
      between DashUserModel and Group.
    - DashUserPermissions: Intermediate model for the ManyToMany relationship 
      between DashUserModel and Permission.
"""

from django.db import models
from django.contrib.auth.models import BaseUserManager
from ...abstract.soft_delete_model import SoftDeleteModel


class DashUserModelManager(BaseUserManager):
    """
    Custom manager for DashUserModel.

    This manager provides helper methods to create users and superusers with 
    the necessary fields, including password handling.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.

        Args:
            email (str): The email address of the user.
            password (str, optional): The password for the user.
            extra_fields (dict, optional): Additional fields for user creation.

        Returns:
            DashUserModel: The created user instance.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.

        Args:
            email (str): The email address of the superuser.
            password (str, optional): The password for the superuser.
            extra_fields (dict, optional): Additional fields for superuser creation.

        Returns:
            DashUserModel: The created superuser instance.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

    class Meta:
        """
        Meta options for DashUser.
        """
        indexes = [
            models.Index(fields=['deleted_at']),
        ]


class DashUserModel(SoftDeleteModel, BaseUserManager):
    """
    Custom user model for the Dash application.

    This model includes custom fields for user roles (student, instructor, admin),
    a biography field, and timestamps for tracking the user's creation, update,
    and soft deletion times.

    Fields:
        - email: The email address of the user (unique).
        - password: The password field (hashed).
        - first_name: The first name of the user.
        - last_name: The last name of the user.
        - role: The role of the user (student, instructor, admin).
        - bio: A short biography about the user.
        - created_at: The timestamp when the user was created.
        - updated_at: The timestamp when the user was last updated.
        - deleted_at: The timestamp when the user was soft-deleted (null if active).
    """
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    )

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='student')
    bio = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='dashuser_set',
        blank=True,
        through='DashUserGroups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='dashuser_set',
        blank=True,
        through='DashUserPermissions'
    )

    objects = DashUserModelManager()

    class Meta:
        """
        Meta options for DashUserModel.
        """
        db_table = 'dash_users'

    def __str__(self):
        """
        Return a string representation of the user model instance.

        This method returns the email of the user as the string representation
        for the DashUserModel instance.
        """
        return str(self.email) if self.email else "No Email"


class DashUserGroups(models.Model):
    """
    Custom intermediate model for the ManyToMany relationship between
    DashUserModel and Group.

    This model links users to groups and is used for associating DashUserModel
    instances with Django's built-in Group model.
    """
    user = models.ForeignKey(DashUserModel, on_delete=models.CASCADE)
    group = models.ForeignKey('auth.Group', on_delete=models.CASCADE)

    class Meta:
        """
        Meta options for DashUserGroups.

        This specifies the database table name for the intermediate model, 
        which is 'dash_users_groups'.
        """
        db_table = 'dash_users_groups'


class DashUserPermissions(models.Model):
    """
    Custom intermediate model for the ManyToMany relationship between
    DashUserModel and Permission.

    This model links users to permissions and is used for associating DashUserModel
    instances with Django's built-in Permission model.
    """
    user = models.ForeignKey(DashUserModel, on_delete=models.CASCADE)
    permission = models.ForeignKey('auth.Permission', on_delete=models.CASCADE)

    class Meta:
        """
        Meta options for DashUserPermissions.

        This specifies the database table name for the intermediate model, 
        which is 'dash_users_permissions'.
        """
        db_table = 'dash_users_permissions'
