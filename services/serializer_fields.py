"""The services serializer fields module."""

from rest_framework import serializers

from professionals.models import ProfessionalLocation

from .models import Service


# TODO: test it
class AccountServiceForeignKey(serializers.PrimaryKeyRelatedField):
    """The service field filtered by the request user."""

    def get_queryset(self):
        """Return the queryset."""
        user = self.context['request'].user
        return Service.objects.get_user_list(user=user)


class AccountProfessionalLocationForeignKey(
        serializers.PrimaryKeyRelatedField, ):
    """The professional location field filtered by the request user."""

    def get_queryset(self):
        """Return the queryset."""
        user = self.context['request'].user
        return ProfessionalLocation.objects.get_user_list(user=user)
