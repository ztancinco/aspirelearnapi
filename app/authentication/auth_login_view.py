"""
Login related views.
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
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
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        'access_token': str(refresh.access_token),
                        'refresh_token': str(refresh),
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
