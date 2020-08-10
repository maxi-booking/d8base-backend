"""The managers test module."""

from datetime import time

import arrow
import pytest
from django.db.models import QuerySet

from schedule.models import (ProfessionalClosedPeriod, ProfessionalSchedule,
                             ServiceClosedPeriod, ServiceSchedule)

pytestmark = pytest.mark.django_db


def test_service_closed_periods_manager_get_overlapping_entries(
        service_closed_periods: QuerySet):
    """Should return overlapping closed periods."""
    manager = ServiceClosedPeriod.objects
    period = service_closed_periods.first()
    assert not manager.get_overlapping_entries(period).count()
    period.start_datetime = arrow.utcnow().shift(days=+1).datetime
    period.end_datetime = arrow.utcnow().shift(days=+15).datetime
    assert manager.get_overlapping_entries(period).count()

    period.start_datetime = arrow.utcnow().shift(days=+6).datetime
    period.end_datetime = arrow.utcnow().shift(days=+12).datetime
    assert manager.get_overlapping_entries(period).count()


def test_professional_closed_periods_manager_get_overlapping_entries(
        professional_closed_periods: QuerySet):
    """Should return overlapping closed periods."""
    manager = ProfessionalClosedPeriod.objects
    period = professional_closed_periods.first()
    assert not manager.get_overlapping_entries(period).count()
    period.start_datetime = arrow.utcnow().shift(days=+1).datetime
    period.end_datetime = arrow.utcnow().shift(days=+15).datetime
    assert manager.get_overlapping_entries(period).count()

    period.start_datetime = arrow.utcnow().shift(days=+6).datetime
    period.end_datetime = arrow.utcnow().shift(days=+12).datetime
    assert manager.get_overlapping_entries(period).count()


def test_professional_schedule_manager_get_overlapping_entries(
        professional_schedules: QuerySet):
    """Should return overlapping schedules."""
    manager = ProfessionalSchedule.objects
    schedule = professional_schedules.first()
    assert not manager.get_overlapping_entries(schedule).count()
    schedule.start_time = time(3)
    schedule.end_time = time(23)
    assert manager.get_overlapping_entries(schedule).count()

    schedule.start_time = time(16)
    schedule.end_time = time(23)
    assert manager.get_overlapping_entries(schedule).count()


def test_service_schedule_manager_get_overlapping_entries(
        service_schedules: QuerySet):
    """Should return overlapping schedules."""
    manager = ServiceSchedule.objects
    schedule = service_schedules.first()
    assert not manager.get_overlapping_entries(schedule).count()
    schedule.start_time = time(3)
    schedule.end_time = time(23)
    assert manager.get_overlapping_entries(schedule).count()
