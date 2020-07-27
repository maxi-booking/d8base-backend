"""The schedule models module."""

from typing import Iterable

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from d8b.fields import DayOfWeekField
from d8b.models import CommonInfo, ValidationMixin
from d8b.validators import validate_datetime_in_future

from .managers import (ProfessionalClosedPeriodManager,
                       ProfessionalScheduleManager, ServiceClosedPeriodManager,
                       ServiceScheduleManager)
from .validators import (validate_professional_closed_period,
                         validate_professional_schedule,
                         validate_schedule_time_span,
                         validate_service_closed_period,
                         validate_service_schedule)


class Schedule(CommonInfo, ValidationMixin):
    """The base schedule class."""

    day_of_week = DayOfWeekField(
        verbose_name=_("day of week"),
        db_index=True,
    )
    start_time = models.TimeField(
        verbose_name=_("start time"),
        db_index=True,
        default=settings.SCHEDULE_START_TIME,
        validators=[validate_schedule_time_span],
    )
    end_time = models.TimeField(
        verbose_name=_("end time"),
        db_index=True,
        default=settings.SCHEDULE_END_TIME,
        validators=[validate_schedule_time_span],
    )
    is_enabled = models.BooleanField(
        default=True,
        verbose_name=_("is enabled?"),
        db_index=True,
    )

    def __str__(self) -> str:
        """Return the string representation."""
        day = self.get_day_of_week_display()
        return f"{day}: {self.start_time}-{self.end_time}"

    class Meta(CommonInfo.Meta):
        """The metainformation."""

        ordering: Iterable[str] = ("day_of_week", "start_time")
        abstract = True


class ClosedPeriod(CommonInfo, ValidationMixin):
    """The closed period class."""

    start_datetime = models.DateTimeField(
        verbose_name=_("start datetime"),
        validators=[validate_datetime_in_future],
        db_index=True,
    )
    end_datetime = models.DateTimeField(
        verbose_name=_("end datetime"),
        validators=[validate_datetime_in_future],
        db_index=True,
    )
    is_enabled = models.BooleanField(
        default=True,
        verbose_name=_("is enabled?"),
        db_index=True,
    )

    def __str__(self) -> str:
        """Return the string representation."""
        return f"{self.start_datetime}-{self.end_datetime}"

    class Meta(CommonInfo.Meta):
        """The metainformation."""

        ordering: Iterable[str] = ("start_datetime", "end_datetime")
        abstract = True


class ProfessionalSchedule(Schedule):
    """The professional schedule class."""

    validators = [validate_professional_schedule]

    objects = ProfessionalScheduleManager()

    professional = models.ForeignKey(
        "professionals.Professional",
        on_delete=models.CASCADE,
        related_name="schedule",
        verbose_name=_("professional"),
    )

    class Meta(Schedule.Meta):
        """The metainformation."""

        abstract = False


class ServiceSchedule(Schedule):
    """The professional schedule class."""

    validators = [validate_service_schedule]

    objects = ServiceScheduleManager()

    service = models.ForeignKey(
        "services.Service",
        on_delete=models.CASCADE,
        related_name="schedule",
        verbose_name=_("service"),
    )

    class Meta(Schedule.Meta):
        """The metainformation."""

        abstract = False


class ProfessionalClosedPeriod(ClosedPeriod):
    """The professional closed period class."""

    validators = [validate_professional_closed_period]

    objects = ProfessionalClosedPeriodManager()

    professional = models.ForeignKey(
        "professionals.Professional",
        on_delete=models.CASCADE,
        related_name="closed_periods",
        verbose_name=_("professional"),
    )

    class Meta(ClosedPeriod.Meta):
        """The metainformation."""

        abstract = False


class ServiceClosedPeriod(ClosedPeriod):
    """The service closed period class."""

    validators = [validate_service_closed_period]

    objects = ServiceClosedPeriodManager()

    service = models.ForeignKey(
        "services.Service",
        on_delete=models.CASCADE,
        related_name="closed_periods",
        verbose_name=_("service"),
    )

    class Meta(ClosedPeriod.Meta):
        """The metainformation."""

        abstract = False


# class TimeOffset(CommonInfo, ValidationMixin):
#     """The calendar entry class."""

#     class Meta(CommonInfo.Meta):
#         """The metainformation."""

#         abstract = True
