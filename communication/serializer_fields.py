"""The professional serializer fields module."""

from rest_framework import serializers

from .models import Message


class ParentMessageForeignKey(serializers.PrimaryKeyRelatedField):
    """The parent message field filtered by the request user."""

    def get_queryset(self):
        """Return the queryset."""
        user = self.context['request'].user
        return Message.objects.get_received_messages(user=user)
