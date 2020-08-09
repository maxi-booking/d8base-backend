"""The schedule serializers module."""
from d8b.serializers import ModelCleanFieldsSerializer
from professionals.serializer_fields import AccountProfessionalForeignKey
from services.serializer_fields import AccountServiceForeignKey

from .models import (ProfessionalClosedPeriod, ProfessionalSchedule,
                     ServiceClosedPeriod, ServiceSchedule)


class ServiceClosedPeriodSerializer(ModelCleanFieldsSerializer):
    """The service closed period serializer."""

    class Meta:
        """The metainformation."""

        model = ServiceClosedPeriod

        fields = ("id", "start_datetime", "end_datetime", "is_enabled",
                  "service", "created", "modified", "created_by",
                  "modified_by")
        read_only_fields = ("created", "modified", "created_by", "modified_by")


class ProfessionalClosedPeriodSerializer(ModelCleanFieldsSerializer):
    """The professional closed period serializer."""

    class Meta:
        """The metainformation."""

        model = ProfessionalClosedPeriod

        fields = ("id", "start_datetime", "end_datetime", "is_enabled",
                  "professional", "created", "modified", "created_by",
                  "modified_by")
        read_only_fields = ("created", "modified", "created_by", "modified_by")


class ProfessionalScheduleSerializer(ModelCleanFieldsSerializer):
    """The professional schedule serializer."""

    professional = AccountProfessionalForeignKey(required=True)

    class Meta:
        """The metainformation."""

        model = ProfessionalSchedule

        fields = ("id", "day_of_week", "get_day_of_week_display", "start_time",
                  "end_time", "is_enabled", "professional", "created",
                  "modified", "created_by", "modified_by")
        read_only_fields = ("created", "modified", "created_by", "modified_by")


class ServiceScheduleSerializer(ModelCleanFieldsSerializer):
    """The service schedule serializer."""

    service = AccountServiceForeignKey(required=True)

    class Meta:
        """The metainformation."""

        model = ServiceSchedule

        fields = ("id", "day_of_week", "get_day_of_week_display", "start_time",
                  "end_time", "is_enabled", "service", "created", "modified",
                  "created_by", "modified_by")
        read_only_fields = ("created", "modified", "created_by", "modified_by")
