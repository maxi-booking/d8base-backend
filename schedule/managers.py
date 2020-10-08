"""The services managers module."""
from collections import defaultdict
from typing import TYPE_CHECKING, DefaultDict, List, Optional

import arrow
from django.db import models
from django.db.models.query import QuerySet

if TYPE_CHECKING:
    from professionals.models import Professional
    from services.models import Service
    from .models import (ProfessionalSchedule, ServiceSchedule,
                         AvailabilitySlot, ProfessionalClosedPeriod,
                         ServiceClosedPeriod)


class AvailabilitySlotManager(models.Manager):
    """The availability slot manager."""

    def get_list(self) -> QuerySet:
        """Return a list of objects."""
        return self.all().select_related(
            "professional__user",
            "professional",
            "service",
        )

    def get_overlapping_entries(
        self,
        slot: "AvailabilitySlot",
    ) -> QuerySet:
        """Return the overlapping entries."""
        query = self.get_list().filter(
            start_datetime__lt=slot.end_datetime,
            end_datetime__gt=slot.start_datetime,
            professional=slot.professional,
            service=slot.service,
        )
        if slot.pk:
            query = query.exclude(pk=slot.pk)
        return query

    def get_between_dates(
        self,
        start: arrow.Arrow,
        end: arrow.Arrow,
        professional: "Professional",
        service: Optional["Professional"] = None,
    ) -> QuerySet:
        """Return between the dates."""
        query = self.filter(
            professional=professional,
            start_datetime__lte=end.datetime,
            end_datetime__gte=start.datetime,
        )
        if service:
            query = query.filter(service=service)
        else:
            query = query.filter(service__isnull=True)

        return query


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

    def get_between_dates(
        self,
        start: arrow.Arrow,
        end: arrow.Arrow,
        professional: "Professional",
    ) -> QuerySet:
        """Return between the dates."""
        return self.get_list().filter(
            start_datetime__lt=end.datetime,
            end_datetime__gt=start.datetime,
            professional=professional,
            is_enabled=True,
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

    def get_by_days(
        self,
        professional: "Professional",
    ) -> DefaultDict[int, List["ProfessionalSchedule"]]:
        """Get professional schedules grouped by days."""
        result = defaultdict(list)
        schedules = self.get_list().filter(
            professional=professional,
            is_enabled=True,
        ).order_by("day_of_week", "start_time")
        for entry in schedules:
            result[entry.day_of_week].append(entry)
        return result

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

    def get_by_days(
        self,
        service: "Service",
    ) -> DefaultDict[int, List["ServiceSchedule"]]:
        """Get professional schedules grouped by days."""
        result = defaultdict(list)
        schedules = self.get_list().filter(
            service=service,
            is_enabled=True,
        ).order_by("day_of_week", "start_time")
        for entry in schedules:
            result[entry.day_of_week].append(entry)
        return result


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

    def get_between_dates(
        self,
        start: arrow.Arrow,
        end: arrow.Arrow,
        service: "Service",
    ) -> QuerySet:
        """Return between the dates."""
        return self.get_list().filter(
            start_datetime__lt=end.datetime,
            end_datetime__gt=start.datetime,
            service=service,
            is_enabled=True,
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
