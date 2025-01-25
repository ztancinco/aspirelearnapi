"""
Serializer for Auth
"""
from rest_framework import serializers

class AuthSerializer(serializers.Serializer):
    """
    Serializer for authenticating users by validating username and password.
    """
    username = serializers.CharField(
        max_length=255,
        required=True,
        help_text="The username of the user."
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=6,
        help_text="The password of the user. It will not be returned in responses."
    )

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
