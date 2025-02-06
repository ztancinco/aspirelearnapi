"""
Service for Users
"""

from typing import List, Dict, Any
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Group
from django.db.models import QuerySet, Q
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.functions import Lower
from ..users.serializers.user_serializer import UserSerializer

class DashUsersService:
    """
    Service class for handling user-related operations using Django's built-in User model.
    """

    def get_all_users(self) -> List[Dict[str, Any]]:
        """
        Retrieve all users who have a valid role.

        :return: A list of serialized user data.
        """
        users: QuerySet[User] = User.objects.filter(
            Q(groups__name__iexact='admin') |
            Q(groups__name__iexact='instructor') |
            Q(groups__name__iexact='student')
        ).annotate(
            lower_group_name=Lower('groups__name')
        ).filter(
            Q(lower_group_name='admin') |
            Q(lower_group_name='instructor') |
            Q(lower_group_name='student')
        ).distinct()

        return UserSerializer(users, many=True).data

    def get_user_by_id(self, user_id: int) -> Dict[str, Any]:
        """
        Retrieve a user by its ID and serialize it.

        :param user_id: ID of the user to retrieve
        :return: Serialized user data
        """
        user: User = get_object_or_404(User, id=user_id)
        return UserSerializer(user).data

    def create_user(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new user.

        :param data: Dictionary containing user data
        :return: Serialized user data
        """
        if 'role' in data:
            role = data['role'].capitalize()
            try:
                group = Group.objects.get(name=role)
                data['groups'] = [group]
            except ObjectDoesNotExist as exc:
                raise ValueError(f"Group with name {role} does not exist.") from exc

        # Create the user
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Add the user to the group
        if 'groups' in data:
            user.groups.add(*data['groups'])
            user.save()

        return serializer.data

    def update_user(self, user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing user.

        :param user_id: ID of the user to update
        :param data: Dictionary containing updated user data
        :return: Serialized updated user data
        """
        user: User = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def delete_user(self, user_id: int) -> None:
        """
        Soft delete a user by its ID.

        :param user_id: ID of the user to delete
        """
        user: User = get_object_or_404(User, id=user_id)
        user.delete()
