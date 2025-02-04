"""
Login related views.
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .auth_serializer import AuthSerializer


class AuthLoginView(APIView):
    """
    View to handle user authentication and token generation.
    """

    def post(self, request):
        """
        POST method to authenticate user and generate access and refresh tokens.
        """
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # Retrieve the user by email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:  # pylint: disable=no-member
                return Response(
                    {'error': 'Invalid credentials'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Retrieve user's groups as roles
            groups = user.groups.values_list('name', flat=True)  # Get group names
            roles = list(groups)  # Convert queryset to list

            # Authenticate using the username (required by `authenticate`)
            user = authenticate(username=user.username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)

                user_data = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'roles': roles,  # Include groups as roles
                    'is_active': user.is_active,
                    'date_joined': user.date_joined,
                }

                return Response(
                    {
                        'access_token': str(refresh.access_token),
                        'refresh_token': str(refresh),
                        'user': user_data,
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
