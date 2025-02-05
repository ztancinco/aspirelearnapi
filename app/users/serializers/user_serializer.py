"""
Serializer for DashUser Model.
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for Django's built-in User model to handle serialization and validation of user data.
    """
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    bio = serializers.CharField(allow_blank=True, required=False)

    # Dynamically adding the role field
    role = serializers.SerializerMethodField()

    class Meta:
        """
        Meta options for UserSerializer.
        """
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',  # Role is added as a dynamic field
            'bio',
            'is_active',
            'date_joined',
        ]
        read_only_fields = ['id', 'date_joined']

    def validate_email(self, value):
        """
        Custom validation for email field to ensure uniqueness.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def get_role(self, obj):
        """
        Custom method to determine the user's role based on group membership.
        """
        group_names = obj.groups.values_list('name', flat=True)

        if 'admin' in group_names:
            return 'admin'
        if 'instructor' in group_names:
            return 'instructor'
        if 'student' in group_names:
            return 'student'
        return 'unknown'
