"""The communication serializers module."""
from rest_framework import serializers
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from d8b.serializers import ModelCleanFieldsSerializer
from users.models import User
from users.serializers import UserHiddenFieldMixin

from .models import Message, Review, ReviewComment, SuggestedMessage
from .serializer_fields import ParentMessageForeignKey, UserReviewForeignKey


class SuggestedMessageSerializer(
        serializers.ModelSerializer,
        CacheResponseMixin,
):
    """The suggested answer serializer."""

    class Meta:
        """The metainformation."""

        model = SuggestedMessage

        fields = ("id", "name", "body", "subcategory", "is_enabled")
        read_only_fields = ("created", "modified", "created_by", "modified_by")


class ReviewCommentSerializer(
        ModelCleanFieldsSerializer,
        UserHiddenFieldMixin,
):
    """The review comment serializer."""

    review = UserReviewForeignKey()

    class Meta:
        """The metainformation."""

        model = ReviewComment

        fields = ("id", "user", "review", "title", "description", "created",
                  "modified", "created_by", "modified_by")
        read_only_fields = ("created", "modified", "created_by", "modified_by")


class ReviewSerializer(ModelCleanFieldsSerializer, UserHiddenFieldMixin):
    """The review serializer."""

    class Meta:
        """The metainformation."""

        model = Review

        fields = ("id", "user", "professional", "title", "description",
                  "rating", "created", "modified", "created_by", "modified_by")
        read_only_fields = ("created", "modified", "created_by", "modified_by")


class UserSerializer(serializers.ModelSerializer):
    """The message sender or recipient serializer."""

    avatar_thumbnail = serializers.ImageField(read_only=True)
    avatar = serializers.ImageField(read_only=True)

    class Meta:
        """The metainformation."""

        model = User

        fields = ("id", "email", "first_name", "last_name", "avatar",
                  "avatar_thumbnail")


class LatestMessageSerializer(serializers.ModelSerializer):
    """The latest received message serializer."""

    sender = UserSerializer(many=False, read_only=True)
    recipient = UserSerializer(many=False, read_only=True)

    class Meta:
        """The professional list class serializer META class."""

        model = Message

        fields = ("id", "sender", "recipient", "subject", "body", "is_read",
                  "read_datetime", "created", "modified", "created_by",
                  "modified_by")
        read_only_fields = ("read_datetime", "is_read", "created", "modified",
                            "created_by", "modified_by")


class MessageSerializer(serializers.ModelSerializer):
    """The message serializer."""

    class Meta:
        """The metainformation."""

        model = Message

        fields = ("id", "sender", "recipient", "parent", "subject", "body",
                  "is_read", "read_datetime", "created", "modified",
                  "created_by", "modified_by")
        read_only_fields = ("sender", "recipient", "read_datetime", "is_read",
                            "created", "modified", "created_by", "modified_by")


class SentMessageSerializer(ModelCleanFieldsSerializer):
    """The sent message serializer."""

    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())
    parent = ParentMessageForeignKey(required=False, allow_null=True)

    class Meta:
        """The professional location class serializer META class."""

        model = Message

        fields = ("id", "sender", "recipient", "parent", "subject", "body",
                  "is_read", "read_datetime", "created", "modified",
                  "created_by", "modified_by")
        read_only_fields = ("read_datetime", "is_read", "created", "modified",
                            "created_by", "modified_by")


class ReceivedMessageSerializer(ModelCleanFieldsSerializer):
    """The received message serializer."""

    recipient = serializers.HiddenField(
        default=serializers.CurrentUserDefault())
    parent = ParentMessageForeignKey(required=False, allow_null=True)

    class Meta:
        """The professional location class serializer META class."""

        model = Message

        fields = ("id", "sender", "recipient", "parent", "subject", "body",
                  "is_read", "read_datetime", "created", "modified",
                  "created_by", "modified_by")
        read_only_fields = ("read_datetime", "is_read", "created", "modified",
                            "created_by", "modified_by")
