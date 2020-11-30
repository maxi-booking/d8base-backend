"""The search serializers module."""
from rest_framework import serializers

from professionals.serializers import ProfessionalListSerializer
from services.serializers import ServiceListSerializer


class SearchSerializer(serializers.Serializer):
    """The professional calendar serializer."""

    # pylint: disable=abstract-method
    professional = ProfessionalListSerializer(many=False, read_only=True)
    services = ServiceListSerializer(many=True, read_only=True)
