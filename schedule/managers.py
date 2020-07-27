"""The services managers module."""
from typing import TYPE_CHECKING

from django.db import models
from django.db.models.query import QuerySet

if TYPE_CHECKING:
    from .models import (ProfessionalSchedule, ServiceSchedule,
                         ProfessionalClosedPeriod, ServiceClosedPeriod)


class ProfessionalClosedPeriodManager(models.Manager):
    """The professional closed period manager."""

    def get_list(self) -> QuerySet:
        """Return a list of objects."""
        return self.all().select_related(
            "professional__user",
            "professional",
            "created_by",
            "modified_by",
        )

    def get_overlapping_entries(
        self,
        period: "ProfessionalClosedPeriod",
    ) -> QuerySet:
        """Return the overlapping entries."""
        query = self.get_list().filter(
            start_datetime__lt=period.end_datetime,
            end_datetime__gt=period.start_datetime,
            professional=period.professional,
        )
        if period.pk:
            query = query.exclude(pk=period.pk)
        return query


class ProfessionalScheduleManager(models.Manager):
    """The professional schedule manager."""

    def get_list(self) -> QuerySet:
        """Return a list of objects."""
        return self.all().select_related(
            "professional__user",
            "professional",
            "created_by",
            "modified_by",
        )

    def get_overlapping_entries(
        self,
        schedule: "ProfessionalSchedule",
    ) -> QuerySet:
        """Return the overlapping entries."""
        query = self.get_list().filter(
            start_time__lt=schedule.end_time,
            end_time__gt=schedule.start_time,
            day_of_week=schedule.day_of_week,
            professional=schedule.professional,
        )
        if schedule.pk:
            query = query.exclude(pk=schedule.pk)
        return query


class ServiceScheduleManager(models.Manager):
    """The service schedule manager."""

    def get_list(self) -> QuerySet:
        """Return a list of objects."""
        return self.all().select_related(
            "service",
            "service__professional__user",
            "service__professional",
            "created_by",
            "modified_by",
        )

    def get_overlapping_entries(
        self,
        schedule: "ServiceSchedule",
    ) -> QuerySet:
        """Return the overlapping entries."""
        query = self.get_list().filter(
            start_time__lt=schedule.end_time,
            end_time__gt=schedule.start_time,
            day_of_week=schedule.day_of_week,
            service=schedule.service,
        )
        if schedule.pk:
            query = query.exclude(pk=schedule.pk)
        return query


class ServiceClosedPeriodManager(models.Manager):
    """The service closed period manager."""

    def get_list(self) -> QuerySet:
        """Return a list of objects."""
        return self.all().select_related(
            "service",
            "service__professional__user",
            "service__professional",
            "created_by",
            "modified_by",
        )

    def get_overlapping_entries(
        self,
        period: "ServiceClosedPeriod",
    ) -> QuerySet:
        """Return the overlapping entries."""
        query = self.get_list().filter(
            start_datetime__lt=period.end_datetime,
            end_datetime__gt=period.start_datetime,
            service=period.service,
        )
        if period.pk:
            query = query.exclude(pk=period.pk)
        return query
