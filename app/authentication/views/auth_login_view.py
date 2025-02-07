"""
Login related views.
"""

import base64
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from drf_spectacular.utils import extend_schema
from ..serializers.auth_serializer import AuthSerializer

User = get_user_model()


class AuthLoginView(APIView):
    """
    View to handle user authentication and token generation.
    """

    @extend_schema(
        request=AuthSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "access_token": {"type": "string"},
                    "refresh_token": {"type": "string"},
                    "user": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "username": {"type": "string"},
                            "email": {"type": "string"},
                            "first_name": {"type": "string"},
                            "last_name": {"type": "string"},
                            "roles": {"type": "array", "items": {"type": "string"}},
                            "is_active": {"type": "boolean"},
                            "date_joined": {"type": "string", "format": "date-time"},
                        },
                    },
                },
            },
            400: {"type": "object", "properties": {"error": {"type": "string"}}},
            401: {"type": "object", "properties": {"error": {"type": "string"}}},
        },
    )
    def post(self, request):
        """
        POST method to authenticate user and generate access and refresh tokens.
        """
        request_data = request.data.copy()

        try:
            request_data["password"] = base64.b64decode(
                request_data["password"]
            ).decode("utf-8")
        except (base64.binascii.Error, UnicodeDecodeError):
            return Response(
                {"error": "Invalid password format"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AuthSerializer(data=request_data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            # Retrieve the user by email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # Retrieve user's groups as roles
            roles = list(
                user.groups.values_list("name", flat=True)
            )  # Convert queryset to list

            # Authenticate using username (Django requires `username`)
            user = authenticate(username=user.username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)

                user_data = {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "roles": roles,  # Include groups as roles
                    "is_active": user.is_active,
                    "date_joined": user.date_joined,
                }

                return Response(
                    {
                        "access_token": str(refresh.access_token),
                        "refresh_token": str(refresh),
                        "user": user_data,
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
