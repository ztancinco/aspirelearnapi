"""
Base Serializer for User.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class BaseUserSerializer(serializers.ModelSerializer):
    """
    Serializer for Django's built-in User model to handle serialization of user (instructor) data.
    """
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    bio = serializers.CharField(allow_blank=True, required=False)
    role = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        """
        Meta options for InstructorSerializer.
        """
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'bio',
            'is_active',
            'date_joined',
            'password',
        ]
        read_only_fields = ['id', 'date_joined']

    def get_role(self, obj):
        """
        Custom method to determine the user's role based on group membership.
        """
        group_names = list(
            obj.groups.values_list('name', flat=True)
        )

        group_names = [name.lower() for name in group_names]

        if 'admin' in group_names:
            return 'Admin'
        if 'instructor' in group_names:
            return 'Instructor'
        if 'student' in group_names:
            return 'Student'
        return None

    def create(self, validated_data):
        """
        Override the create method to handle password hashing.
        """
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
