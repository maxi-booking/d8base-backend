"""The services validators module."""
from datetime import time
from typing import TYPE_CHECKING

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from .models import (ProfessionalSchedule, ServiceSchedule, Schedule,
                         AvailabilitySlot, ProfessionalClosedPeriod,
                         ServiceClosedPeriod, ClosedPeriod)


def validate_schedule_time_span(val: time):
    """Validate the schedule span of time."""
    span = settings.SCHEDULE_MINIMAL_TIME_SPAN
    if val.minute == 59 and val.hour == 23:
        return
    if val.second != 0 or val.microsecond != 0 or val.minute % span != 0:
        raise ValidationError(_(f"The minimal time interval is {span}"))


def _validate_schedule(schedule: "Schedule"):
    """Validate the schedule."""
    try:
        model = apps.get_model("schedule", schedule.__class__.__name__)
        if not schedule.start_time or not schedule.end_time:
            raise ValidationError(_("The time interval is not set"))
        if schedule.start_time >= schedule.end_time:
            raise ValidationError(_("The interval is incorrect"))
        if model.objects.get_overlapping_entries(schedule).count():
            raise ValidationError(_("Time intervals should not overlap"))
    except ObjectDoesNotExist:
        raise ValidationError(_("The owner is empty"))


def validate_professional_schedule(schedule: "ProfessionalSchedule"):
    """Validate the professional schedule."""
    _validate_schedule(schedule)


def validate_service_schedule(schedule: "ServiceSchedule"):
    """Validate the service schedule."""
    _validate_schedule(schedule)


def _validate_closed_period(period: "ClosedPeriod"):
    """Validate the closed period."""
    try:
        model = apps.get_model("schedule", period.__class__.__name__)
        if not period.start_datetime or not period.end_datetime:
            raise ValidationError(_("The interval is not set"))
        if period.start_datetime >= period.end_datetime:
            raise ValidationError(_("The interval is incorrect"))
        if model.objects.get_overlapping_entries(period).count():
            raise ValidationError(_("Datetime intervals should not overlap"))
    except ObjectDoesNotExist:
        raise ValidationError(_("The owner is empty"))


def validate_professional_closed_period(period: "ProfessionalClosedPeriod"):
    """Validate the professional closed period."""
    _validate_closed_period(period)


def validate_service_closed_period(period: "ServiceClosedPeriod"):
    """Validate the service closed period."""
    _validate_closed_period(period)


def validate_availability_slot(slot: "AvailabilitySlot"):
    """Validate the availability slot."""
    _validate_closed_period(slot)
