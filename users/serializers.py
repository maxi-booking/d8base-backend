"""The users serializers module."""
from typing import Dict

from django.conf import settings
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from .models import User, UserLanguage
from .registration import get_auth_tokens


class ProfileSerializer(serializers.ModelSerializer):
    """The profile serializer."""

    class Meta:
        """The profile class serializer META class."""

        model = User
        fields = settings.USER_FIELDS
        read_only_fields = settings.USER_READONLY_FIELDS + ['email']


class RegisterTokenSerializer(serializers.ModelSerializer):
    """The registration serializer with the user token included."""

    token = serializers.SerializerMethodField('get_token')

    # pylint: disable=no-self-use
    @swagger_serializer_method(serializer_or_field=serializers.DictField)
    def get_token(self, user: User) -> Dict[str, str]:
        """Return the user token."""
        access, refresh = get_auth_tokens(user)
        return {'access': access, 'refresh': refresh}

    class Meta:
        """The register class serializer META class."""

        model = User
        fields = settings.USER_FIELDS + ['token']
        read_only_fields = settings.USER_READONLY_FIELDS


class UserHiddenFieldMixin(serializers.Serializer):
    """Mixin with a hidden user field."""

    # pylint: disable=abstract-method
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


class UserLanguageSerializer(
        UserHiddenFieldMixin,
        serializers.ModelSerializer,
):
    """The user language serializer."""

    class Meta:
        """The user language class serializer META class."""

        model = UserLanguage

        fields = ('id', 'user', 'language', 'is_native', 'created', 'modified',
                  'created_by', 'modified_by')
        read_only_fields = ('created', 'modified', 'created_by', 'modified_by')
