"""
Serializer for User.
"""
from django.contrib.auth import get_user_model
from ....abstract.base_user_serializer import BaseUserSerializer

User = get_user_model()

class InstructorSerializer(BaseUserSerializer):
    """
    Serializer for instructors in the system, extending BaseUserSerializer.
    """
