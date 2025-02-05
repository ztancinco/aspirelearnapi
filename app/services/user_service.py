"""
Service for Users
"""

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from ..users.serializers.user_serializer import UserSerializer

class DashUsersService:
    """
    Service class for handling user-related operations using Django's built-in User model.
    """

    def get_all_users(self):
        """
        Retrieve all users and serialize them.
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return serializer.data

    def get_user_by_id(self, user_id):
        """
        Retrieve a user by its ID and serialize it.

        :param user_id: ID of the user to retrieve
        :return: Serialized user data
        """
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user)
        return serializer.data

    def create_user(self, data):
        """
        Create a new user.

        :param data: Dictionary containing user data
        :return: Serialized user data
        """
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def update_user(self, user_id, data):
        """
        Update an existing user.

        :param user_id: ID of the user to update
        :param data: Dictionary containing updated user data
        :return: Serialized updated user data
        """
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def delete_user(self, user_id):
        """
        Soft delete a user by its ID.

        :param user_id: ID of the user to delete
        """
        user = get_object_or_404(User, id=user_id)
        user.delete()
        user.save()
