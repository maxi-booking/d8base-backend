"""The professional serializer fields module."""

from rest_framework import serializers

from .models import Professional


class AccountProfessionalForeignKey(serializers.PrimaryKeyRelatedField):
    """The professional field filtered by the request user."""

    def get_queryset(self):
        """Return the queryset."""
        user = self.context['request'].user
        return Professional.objects.get_user_list(user=user)
