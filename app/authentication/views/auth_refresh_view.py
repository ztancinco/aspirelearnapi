"""
View for refresh auth tokens
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema


@method_decorator(csrf_exempt, name="dispatch")
class AuthRefreshTokenView(APIView):
    """
    View to handle refreshing the access token using a valid refresh token.
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
            200: {
                "type": "object",
                "properties": {
                    "access_token": {
                        "type": "string",
                        "description": "New Access Token",
                    }
                },
            },
            400: {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "description": "Error message"}
                },
            },
            401: {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "description": "Invalid refresh token"}
                },
            },
        },
    )
    def post(self, request):
        """
        POST method to refresh the access token using the provided refresh token.
        """
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)
            return Response(
                {"access_token": new_access_token}, status=status.HTTP_200_OK
            )
        except TokenError:
            return Response(
                {"error": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED
            )
