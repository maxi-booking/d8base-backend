"""The users serializers module."""

from rest_framework import serializers

from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    """The contact serializer."""

    class Meta:
        """The contact class serializer META class."""

        model = Contact
        fields = ("id", "name", "code", "is_default", "countries",
                  "excluded_countries", "created", "modified", "created_by",
                  "modified_by")
        read_only_fields = ("created", "modified", "created_by", "modified_by",
                            "countries", "excluded_countries")
