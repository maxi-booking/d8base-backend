"""The validators test module."""

from datetime import time

import pytest
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import QuerySet

from schedule.validators import (validate_professional_schedule,
                                 validate_schedule_time_span,
                                 validate_service_schedule)

pytestmark = pytest.mark.django_db


def test_validate_schedule_time_span():
    """Should validate a time interval."""
    span = settings.SCHEDULE_MINIMAL_TIME_SPAN
    with pytest.raises(ValidationError):
        validate_schedule_time_span(time(9, int(span * 0.5)))
    with pytest.raises(ValidationError):
        validate_schedule_time_span(time(9, 0, 10))
    with pytest.raises(ValidationError):
        validate_schedule_time_span(time(9, 0, 0, 10))

    validate_schedule_time_span(time(9, span))


def test_validate_professional_schedule(professional_schedules: QuerySet):
    """Should validate a professional schedule."""
    schedule = professional_schedules.first()
    schedule.start_time = time(3)
    schedule.end_time = time(23)
    with pytest.raises(ValidationError):
        validate_professional_schedule(schedule)

    schedule.start_time = time(3)
    schedule.end_time = time(4)
    schedule.professional = None
    with pytest.raises(ValidationError):
        validate_professional_schedule(schedule)


def test_validate_service_schedule(service_schedules: QuerySet):
    """Should validate a service schedule."""
    schedule = service_schedules.first()
    schedule.start_time = time(3)
    schedule.end_time = time(23)
    with pytest.raises(ValidationError):
        validate_service_schedule(schedule)

    schedule.start_time = time(3)
    schedule.end_time = time(4)
    schedule.service = None
    with pytest.raises(ValidationError):
        validate_service_schedule(schedule)
