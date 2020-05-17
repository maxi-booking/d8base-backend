"""The communication serializers module."""
from rest_framework import serializers

from d8b.serializers import ModelCleanFieldsSerializer

from .models import Message
from .serializer_fields import ParentMessageForeignKey


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
