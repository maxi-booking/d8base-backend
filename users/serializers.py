"""The users serializers module."""
from typing import Any, Dict

from django.conf import settings
from drf_extra_fields.fields import Base64ImageField
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from .models import (User, UserContact, UserLanguage, UserLocation,
                     UserSavedProfessional, UserSettings)
from .registration import get_auth_tokens


class UserSerializer(serializers.ModelSerializer):
    """The message sender or recipient serializer."""

    avatar_thumbnail = serializers.ImageField(read_only=True)
    avatar = serializers.ImageField(read_only=True)

    class Meta:
        """The metainformation."""

        model = User

        fields = ("id", "first_name", "public_last_name", "avatar",
                  "avatar_thumbnail")


class UserCalculatedUnitsSerializer(serializers.Serializer):
    """The user calculated units serializer."""

    # pylint: disable=abstract-method
    is_imperial_units = serializers.BooleanField()
    timezone = serializers.CharField()
    distance = serializers.ChoiceField(choices=settings.UNITS)


class ProfileSerializer(serializers.ModelSerializer):
    """The profile serializer."""

    avatar_thumbnail = serializers.ImageField(read_only=True)
    avatar = Base64ImageField(required=False)

    class Meta:
        """The profile class serializer META class."""

        model = User
        fields = settings.USER_FIELDS + ["avatar_thumbnail"]
        read_only_fields = settings.USER_READONLY_FIELDS + ["email"]


class TokenSerializer(serializers.Serializer):
    """The auth token serializer."""

    # pylint: disable=abstract-method

    access_token: str = serializers.CharField()
    expires_in: str = serializers.IntegerField(
        default=settings.OAUTH2_PROVIDER["ACCESS_TOKEN_EXPIRE_SECONDS"])
    token_type: str = serializers.CharField(default="Bearer")
    scope: str = serializers.CharField()
    refresh_token: str = serializers.CharField()


class RegisterTokenSerializer(serializers.ModelSerializer):
    """The registration serializer with the user token included."""

    token = serializers.SerializerMethodField("get_token")

    # pylint: disable=no-self-use
    @swagger_serializer_method(serializer_or_field=serializers.DictField)
    def get_token(self, user: User) -> Dict[str, Any]:
        """Return the user token."""
        access, refresh = get_auth_tokens(user)

        return TokenSerializer({
            "access_token": access.token,
            "scope": access.scope,
            "refresh_token": refresh.token
        }).data

    class Meta:
        """The register class serializer META class."""

        model = User
        fields = settings.USER_FIELDS + ["token"]
        read_only_fields = settings.USER_READONLY_FIELDS


class UserHiddenFieldMixin(serializers.Serializer):
    """Mixin with a hidden user field."""

    # pylint: disable=abstract-method
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


class UserSettingsSerializer(
        UserHiddenFieldMixin,
        serializers.ModelSerializer,
):
    """The user settings serializer."""

    class Meta:
        """The user settings class serializer META class."""

        model = UserSettings

        fields = ("id", "user", "language", "currency", "units",
                  "is_last_name_hidden", "created", "modified", "created_by",
                  "modified_by")
        read_only_fields = ("created", "modified", "created_by", "modified_by")


class UserSavedProfessionalSerializer(
        UserHiddenFieldMixin,
        serializers.ModelSerializer,
):
    """The user saved professional serializer."""

    class Meta:
        """The user saved professional class serializer META class."""

        model = UserSavedProfessional

        fields = ("id", "user", "note", "professional", "created", "modified",
                  "created_by", "modified_by")
        read_only_fields = ("created", "modified", "created_by", "modified_by")


class UserLanguageSerializer(
        UserHiddenFieldMixin,
        serializers.ModelSerializer,
):
    """The user language serializer."""

    class Meta:
        """The user language class serializer META class."""

        model = UserLanguage

        fields = ("id", "user", "language", "is_native", "created", "modified",
                  "created_by", "modified_by")
        read_only_fields = ("created", "modified", "created_by", "modified_by")


class UserContactSerializer(
        UserHiddenFieldMixin,
        serializers.ModelSerializer,
):
    """The user contact serializer."""

    class Meta:
        """The user contact class serializer META class."""

        model = UserContact

        fields = ("id", "user", "contact", "contact_display", "contact_code",
                  "value", "created", "modified", "created_by", "modified_by")
        read_only_fields = ("created", "modified", "created_by", "modified_by")


class UserLocationSerializer(
        UserHiddenFieldMixin,
        serializers.ModelSerializer,
):
    """The user location serializer."""

    class Meta:
        """The user location class serializer META class."""

        model = UserLocation

        fields = ("id", "user", "country", "region", "subregion", "city",
                  "district", "postal_code", "address", "coordinates",
                  "is_default", "units", "timezone", "created", "modified",
                  "created_by", "modified_by")
        read_only_fields = ("created", "modified", "created_by", "modified_by")
