"""
Logout related views.
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from drf_spectacular.utils import extend_schema


class AuthLogoutView(APIView):
    """
    View for logging out a user by blacklisting their refresh token.
    """

    @extend_schema(
        request={
            "type": "object",
            "properties": {
                "refresh_token": {"type": "string", "description": "JWT Refresh Token"}
            },
            "required": ["refresh_token"],
        },
        responses={
            205: {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "example": "Successfully logged out"}
                },
            },
            400: {"type": "object", "properties": {"error": {"type": "string"}}},
        },
    )
    def post(self, request):
        """
        POST method to log out the user by invalidating the refresh token.
        """
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return Response(
                {"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "Successfully logged out"},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except TokenError:
            return Response(
                {"error": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST,
            )
