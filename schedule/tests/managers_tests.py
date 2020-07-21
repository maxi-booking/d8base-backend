"""The managers test module."""

from datetime import time

import pytest
from django.db.models import QuerySet

from schedule.models import ProfessionalSchedule, ServiceSchedule

pytestmark = pytest.mark.django_db


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
