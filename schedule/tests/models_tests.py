"""The models test module."""

import arrow
import pytest
from django.db.models import QuerySet
from django.utils.timezone import get_current_timezone

from schedule.models import AvailabilitySlot, ProfessionalSchedule

pytestmark = pytest.mark.django_db


def test_schedule_save(professionals: QuerySet):
    """Should set a timezone during saving."""
    schedule = ProfessionalSchedule()
    schedule.professional = professionals.first()
    schedule.day_of_week = 0  # type: ignore
    schedule.start_time = arrow.utcnow().datetime
    schedule.end_time = arrow.utcnow().shift(days=1).datetime
    schedule.save()

    assert schedule.timezone == get_current_timezone()


def test_availability_slot_save(services: QuerySet, professionals: QuerySet):
    """Should set a professional during saving."""
    service = services.first()
    slot = AvailabilitySlot()
    slot.service = service
    slot.professional = professionals.exclude(
        pk=service.professional.pk).first()
    slot.start_datetime = arrow.utcnow().datetime
    slot.end_datetime = arrow.utcnow().shift(days=1).datetime
    slot.save()

    assert slot.professional == service.professional
