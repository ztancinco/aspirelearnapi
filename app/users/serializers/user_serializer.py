"""
Serializer for DashUser Model.
"""

from rest_framework import serializers
from ..models.dash_user_model import DashUserModel


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for DashUserModel to handle serialization and validation of user data.
    """

    first_name = serializers.CharField(required=True, allow_blank=False)
    last_name = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        """
        Meta options for UserSerializer.
        """
        model = DashUserModel
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'role',
            'bio',
            'created_at',
            'updated_at',
            'deleted_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']

    def validate_email(self, value):
        """
        Custom validation for email field to ensure uniqueness.
        """
        if DashUserModel.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_role(self, value):
        """
        Custom validation for role field to ensure it is one of the predefined choices.
        """
        if value not in ['student', 'instructor', 'admin']:
            raise serializers.ValidationError("Role must be 'student', 'instructor', or 'admin'.")
        return value
