"""The services validators module."""
from datetime import time
from typing import TYPE_CHECKING

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from .models import ProfessionalSchedule, ServiceSchedule, Schedule


def validate_schedule_time_span(val: time):
    """Validate the schedule span of time."""
    span = settings.SCHEDULE_MINIMAL_TIME_SPAN
    if val.second != 0 or val.microsecond != 0 or val.minute % span != 0:
        raise ValidationError(_(f"The minimal time interval is {span}"))


def _validate_schedule(schedule: "Schedule", model_name: str):
    """Validate the schedule."""
    try:
        model = apps.get_model("schedule", model_name)
        if model.objects.get_overlapping_entries(schedule).count():
            raise ValidationError(_("Time intervals should not overlap"))
    except ObjectDoesNotExist:
        raise ValidationError(_("The owner is empty"))


def validate_professional_schedule(schedule: "ProfessionalSchedule"):
    """Validate the professional schedule."""
    _validate_schedule(schedule, "ProfessionalSchedule")


def validate_service_schedule(schedule: "ServiceSchedule"):
    """Validate the service schedule."""
    _validate_schedule(schedule, "ServiceSchedule")
