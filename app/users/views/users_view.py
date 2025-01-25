"""
View for listing, creating, and deleting users.

This file contains the view class for handling users
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...services.user_service import DashUsersService

class DashUsersView(APIView):
    """
    View for managing users using DashUsersService.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Initialize the parent class first
        # Now instantiate the DashUsersService instance
        self.user_service = DashUsersService()

    def get(self, _, user_id=None):
        """
        Retrieve all users or a single user by ID.
        """
        if user_id:
            user = self.user_service.get_user_by_id(user_id)
            return Response(user, status=status.HTTP_200_OK)
        users = self.user_service.get_all_users()
        return Response(users, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new user.
        """
        user = self.user_service.create_user(request.data)
        return Response(user, status=status.HTTP_201_CREATED)

    def put(self, request, user_id):
        """
        Update an existing user.
        """
        user = self.user_service.update_user(user_id, request.data)
        return Response(user, status=status.HTTP_200_OK)

    def delete(self, _, user_id):
        """
        Soft delete a user by ID.
        """
        self.user_service.delete_user(user_id)
        return Response(
            {"message": "User deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
