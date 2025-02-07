"""
Serializer for User.
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers
from ...abstract.base_user_serializer import BaseUserSerializer

User = get_user_model()


class UserSerializer(BaseUserSerializer):
    """
    Serializer for Django's built-in User model to handle serialization and validation of user data.
    """

    def validate_email(self, value):
        """
        Custom validation for email field to ensure uniqueness.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
