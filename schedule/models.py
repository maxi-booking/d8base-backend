"""The schedule models module."""

from typing import Iterable

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from d8b.fields import DayOfWeekField
from d8b.models import CommonInfo, ValidationMixin

from .managers import ProfessionalScheduleManager, ServiceScheduleManager
from .validators import (validate_professional_schedule,
                         validate_schedule_time_span,
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

    class Meta(CommonInfo.Meta):
        """The metainformation."""

        ordering: Iterable[str] = ("day_of_week", "start_time")
        abstract = True

    def __str__(self) -> str:
        """Return the string representation."""
        day = self.get_day_of_week_display()
        return f"{day}: {self.start_time}-{self.end_time}"


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


# class ClosedPeriod(CommonInfo, ValidationMixin):
#     """The calendar entry class."""

#     class Meta(CommonInfo.Meta):
#         """The metainformation."""

#         abstract = True

# class TimeOffset(CommonInfo, ValidationMixin):
#     """The calendar entry class."""

#     class Meta(CommonInfo.Meta):
#         """The metainformation."""

#         abstract = True
