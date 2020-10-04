"""The validators test module."""

from datetime import time

import arrow
import pytest
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import QuerySet

from schedule.validators import (validate_availability_slot,
                                 validate_professional_closed_period,
                                 validate_professional_schedule,
                                 validate_schedule_time_span,
                                 validate_service_closed_period,
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
    validate_schedule_time_span(time(23, 59))


def test_validate_service_closed_periods(service_closed_periods: QuerySet):
    """Should validate a service closed period."""
    period = service_closed_periods.first()
    period.start_datetime = arrow.utcnow().shift(days=+2).datetime
    period.end_datetime = arrow.utcnow().shift(days=+1).datetime
    with pytest.raises(ValidationError):
        validate_service_closed_period(period)

    period.start_datetime = arrow.utcnow().shift(days=+1).datetime
    period.end_datetime = arrow.utcnow().shift(days=+15).datetime
    with pytest.raises(ValidationError):
        validate_service_closed_period(period)

    period.start_datetime = None
    period.end_datetime = arrow.utcnow().shift(days=+1).datetime
    with pytest.raises(ValidationError):
        validate_service_closed_period(period)

    period.start_datetime = arrow.utcnow().shift(days=+2).datetime
    period.end_datetime = arrow.utcnow().shift(days=+4).datetime
    period.service = None
    with pytest.raises(ValidationError):
        validate_service_closed_period(period)


def test_validate_professional_closed_periods(
        professional_closed_periods: QuerySet):
    """Should validate a professional closed period."""
    period = professional_closed_periods.first()
    period.start_datetime = arrow.utcnow().shift(days=+2).datetime
    period.end_datetime = arrow.utcnow().shift(days=+1).datetime
    with pytest.raises(ValidationError):
        validate_professional_closed_period(period)

    period.start_datetime = arrow.utcnow().shift(days=+1).datetime
    period.end_datetime = arrow.utcnow().shift(days=+15).datetime
    with pytest.raises(ValidationError):
        validate_service_closed_period(period)

    period.start_datetime = None
    period.end_datetime = arrow.utcnow().shift(days=+1).datetime
    with pytest.raises(ValidationError):
        validate_professional_closed_period(period)

    period.start_datetime = arrow.utcnow().shift(days=+2).datetime
    period.end_datetime = arrow.utcnow().shift(days=+4).datetime
    period.professional = None
    with pytest.raises(ValidationError):
        validate_professional_closed_period(period)


def test_validate_professional_schedule(professional_schedules: QuerySet):
    """Should validate a professional schedule."""
    schedule = professional_schedules.first()

    schedule.start_time = time(4)
    schedule.end_time = time(3)
    with pytest.raises(ValidationError):
        validate_professional_schedule(schedule)

    schedule.start_time = time(3)
    schedule.end_time = time(23)
    with pytest.raises(ValidationError):
        validate_professional_schedule(schedule)

    schedule.start_time = None
    schedule.end_time = time(4)
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

    schedule.start_time = time(4)
    schedule.end_time = time(3)
    with pytest.raises(ValidationError):
        validate_professional_schedule(schedule)

    schedule.start_time = time(3)
    schedule.end_time = time(23)
    with pytest.raises(ValidationError):
        validate_service_schedule(schedule)

    schedule.start_time = None
    schedule.end_time = time(4)
    with pytest.raises(ValidationError):
        validate_service_schedule(schedule)

    schedule.start_time = time(3)
    schedule.end_time = time(4)
    schedule.service = None
    with pytest.raises(ValidationError):
        validate_service_schedule(schedule)


def test_validate_availability_slot(availability_slots: QuerySet):
    """Should validate an availability slots."""
    slot = availability_slots.first()
    slot.start_datetime = arrow.utcnow().shift(days=+2).datetime
    slot.end_datetime = arrow.utcnow().shift(days=+1).datetime
    with pytest.raises(ValidationError):
        validate_availability_slot(slot)

    slot.start_datetime = arrow.utcnow().shift(days=+1).datetime
    slot.end_datetime = arrow.utcnow().shift(days=+15).datetime
    with pytest.raises(ValidationError):
        validate_availability_slot(slot)

    slot.start_datetime = None
    slot.end_datetime = arrow.utcnow().shift(days=+1).datetime
    with pytest.raises(ValidationError):
        validate_availability_slot(slot)

    slot.start_datetime = arrow.utcnow().shift(days=+2).datetime
    slot.end_datetime = arrow.utcnow().shift(days=+4).datetime
    slot.professional = None
    with pytest.raises(ValidationError):
        validate_availability_slot(slot)
