"""
View for listing, creating, and deleting users.

This file contains the view class for handling users
"""

from typing import Optional, Any, Dict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...services.user_service import DashUsersService

class UsersView(APIView):
    """
    View for managing users using DashUsersService.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.user_service: DashUsersService = DashUsersService()

    def get(self, _, user_id: Optional[int] = None) -> Response:
        """
        Retrieve all users or a single user by ID.
        """
        if user_id:
            user: Dict[str, Any] = self.user_service.get_user_by_id(user_id)
            return Response(user, status=status.HTTP_200_OK)
        users: list[Dict[str, Any]] = self.user_service.get_all_users()
        return Response(users, status=status.HTTP_200_OK)

    def post(self, request: Any) -> Response:
        """
        Create a new user.
        """
        user: Dict[str, Any] = self.user_service.create_user(request.data)
        return Response(user, status=status.HTTP_201_CREATED)

    def put(self, request: Any, user_id: int) -> Response:
        """
        Update an existing user.
        """
        user: Dict[str, Any] = self.user_service.update_user(user_id, request.data)
        return Response(user, status=status.HTTP_200_OK)

    def delete(self, _, user_id: int) -> Response:
        """
        Soft delete a user by ID.
        """
        self.user_service.delete_user(user_id)
        return Response(
            {"message": "User deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
