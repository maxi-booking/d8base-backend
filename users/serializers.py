"""The users serializers module."""
from django.conf import settings
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """The User class serializer."""

    token = serializers.SerializerMethodField('get_token')

    def get_token(self, user: User) -> str:  # pylint: disable=no-self-use
        """Return the user token."""
        return user.email

    class Meta:
        """The User class serializer META class."""

        model = User
        fields = settings.USER_FIELDS + ['token']
        read_only_fields = settings.USER_READONLY_FIELDS
