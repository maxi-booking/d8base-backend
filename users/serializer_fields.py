"""The users serializer fields module."""

from rest_framework import serializers

from .models import UserLocation


class AccountUserLocationForeignKey(serializers.PrimaryKeyRelatedField):
    """The user location field filtered by the request user."""

    def get_queryset(self):
        """Return the queryset."""
        user = self.context['request'].user
        return UserLocation.objects.get_user_list(user=user)
