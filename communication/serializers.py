"""The communication serializers module."""
from rest_framework import serializers

from d8b.serializers import ModelCleanFieldsSerializer
from users.models import User
from users.serializers import UserHiddenFieldMixin

from .models import Message, Review, ReviewComment
from .serializer_fields import ParentMessageForeignKey, UserReviewForeignKey


class ReviewCommentSerializer(
        ModelCleanFieldsSerializer,
        UserHiddenFieldMixin,
):
    """The review comment serializer."""

    review = UserReviewForeignKey()

    class Meta:
        """The metainformation."""

        model = ReviewComment

        fields = ('id', 'user', 'review', 'title', 'description', 'created',
                  'modified', 'created_by', 'modified_by')
        read_only_fields = ('created', 'modified', 'created_by', 'modified_by')


class ReviewSerializer(ModelCleanFieldsSerializer, UserHiddenFieldMixin):
    """The review serializer."""

    class Meta:
        """The metainformation."""

        model = Review

        fields = ('id', 'user', 'professional', 'title', 'description',
                  'rating', 'created', 'modified', 'created_by', 'modified_by')
        read_only_fields = ('created', 'modified', 'created_by', 'modified_by')


class SenderSerializer(serializers.ModelSerializer):
    """The message sender serializer."""

    avatar_thumbnail = serializers.ImageField(read_only=True)
    avatar = serializers.ImageField(read_only=True)

    class Meta:
        """The metainformation."""

        model = User

        fields = ('id', 'email', 'first_name', 'last_name', 'avatar',
                  'avatar_thumbnail')


class LatestReceivedMessageSerializer(serializers.ModelSerializer):
    """The latest received message serializer."""

    sender = SenderSerializer(many=False, read_only=True)

    class Meta:
        """The professional list class serializer META class."""

        model = Message

        fields = ('id', 'sender', 'recipient', 'subject', 'body', 'is_read',
                  'read_datetime', 'created', 'modified', 'created_by',
                  'modified_by')
        read_only_fields = ('read_datetime', 'is_read', 'created', 'modified',
                            'created_by', 'modified_by')


class SentMessageSerializer(ModelCleanFieldsSerializer):
    """The sent message serializer."""

    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())
    parent = ParentMessageForeignKey(required=False, allow_null=True)

    class Meta:
        """The professional location class serializer META class."""

        model = Message

        fields = ('id', 'sender', 'recipient', 'parent', 'subject', 'body',
                  'is_read', 'read_datetime', 'created', 'modified',
                  'created_by', 'modified_by')
        read_only_fields = ('read_datetime', 'is_read', 'created', 'modified',
                            'created_by', 'modified_by')


class ReceivedMessageSerializer(ModelCleanFieldsSerializer):
    """The received message serializer."""

    recipient = serializers.HiddenField(
        default=serializers.CurrentUserDefault())
    parent = ParentMessageForeignKey(required=False, allow_null=True)

    class Meta:
        """The professional location class serializer META class."""

        model = Message

        fields = ('id', 'sender', 'recipient', 'parent', 'subject', 'body',
                  'is_read', 'read_datetime', 'created', 'modified',
                  'created_by', 'modified_by')
        read_only_fields = ('read_datetime', 'is_read', 'created', 'modified',
                            'created_by', 'modified_by')
