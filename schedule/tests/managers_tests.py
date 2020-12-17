"""The managers test module."""
from datetime import time

import arrow
import pytest
from django.db.models import QuerySet

from schedule.managers import (AvailabilitySlotManager,
                               ProfessionalScheduleManager,
                               ServiceScheduleManager)
from schedule.models import (AvailabilitySlot, ProfessionalClosedPeriod,
                             ProfessionalSchedule, ServiceClosedPeriod,
                             ServiceSchedule)
from users.models import User

pytestmark = pytest.mark.django_db


def test_professional_schedule_manager_delete_for_user(
    professional_schedules: QuerySet,
    user: User,
):
    """Should delete the entries filtered by the user."""
    manager: ProfessionalScheduleManager = ProfessionalSchedule.objects
    assert professional_schedules.filter(professional__user=user).count() == 20

    manager.delete_for_user(
        user=user,
        pk__in=[
            professional_schedules.filter(professional__user=user).values_list(
                "pk", flat=True).first()
        ],
    )
    assert professional_schedules.filter(professional__user=user).count() == 19
    assert professional_schedules.exclude(professional__user=user).count()

    manager.delete_for_user(user=user)

    assert not professional_schedules.filter(professional__user=user).count()
    assert professional_schedules.exclude(professional__user=user).count()


def test_professional_schedule_manager_get_by_days(
        professional_schedules: QuerySet):
    """Should return schedules combined by weekdays."""
    professional = professional_schedules.first().professional
    schedules = ProfessionalSchedule.objects.get_by_days(professional)
    assert len(schedules[0]) == 2
    assert len(schedules[6]) == 0
    for schedule in schedules[1]:
        assert schedule.day_of_week == 1


def test_service_schedule_manager_get_by_days(service_schedules: QuerySet):
    """Should return schedules combined by weekdays."""
    service = service_schedules.first().service
    schedules = ServiceSchedule.objects.get_by_days(service)
    assert len(schedules[0]) == 2
    assert len(schedules[6]) == 0
    for schedule in schedules[1]:
        assert schedule.day_of_week == 1


def test_service_schedule_manager_delete_for_user(
    service_schedules: QuerySet,
    user: User,
):
    """Should delete the entries filtered by the user."""
    manager: ServiceScheduleManager = ServiceSchedule.objects
    assert service_schedules.filter(
        service__professional__user=user).count() == 40

    manager.delete_for_user(
        user=user,
        pk__in=[
            service_schedules.filter(
                service__professional__user=user).values_list(
                    "pk", flat=True).first()
        ],
    )
    assert service_schedules.filter(
        service__professional__user=user).count() == 39
    assert service_schedules.exclude(service__professional__user=user).count()

    manager.delete_for_user(user=user)

    assert not service_schedules.filter(
        service__professional__user=user).count()
    assert service_schedules.exclude(service__professional__user=user).count()


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


def test_availability_slot_manager_get_encompassing_interval(
    availability_slots: QuerySet,
    disable_slots_signals: None,
):
    """Should return entries that encompass the specified interval."""
    # pylint: disable=unused-argument
    service = availability_slots.exclude(service__isnull=True).first().service
    service.is_base_schedule = False
    service.save()
    manager: AvailabilitySlotManager = AvailabilitySlot.objects
    now = arrow.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    result = manager.get_encompassing_interval(now, now.shift(days=1), service)
    assert result.count() == 0

    result = manager.get_encompassing_interval(
        now,
        now.shift(hours=12),
        service,
    )
    assert result.count() == 0

    result = manager.get_encompassing_interval(
        now.shift(hours=12),
        now.shift(hours=17),
        service,
    )
    assert result.count() == 0

    result = manager.get_encompassing_interval(
        now.shift(hours=16),
        now.shift(hours=17),
        service,
    )
    assert result.count() == 0

    result = manager.get_encompassing_interval(
        now.shift(hours=11),
        now.shift(hours=15),
        service,
    )
    assert result.count() == 1

    service.is_base_schedule = True
    service.save()
    result = manager.get_encompassing_interval(
        now.shift(hours=11),
        now.shift(hours=15),
        service,
    )
    assert result.count() == 1
    assert result.first().professional == service.professional
    assert result.first().service is None

    result = manager.get_encompassing_interval(
        now.shift(hours=16),
        now.shift(hours=17),
        service,
    )
    assert result.count() == 1


def test_availability_slot_manager_get_overlapping_entries(
        availability_slots: QuerySet):
    """Should return overlapping slots."""
    manager: AvailabilitySlotManager = AvailabilitySlot.objects
    slot = availability_slots.first()
    assert not manager.get_overlapping_entries(slot).count()
    slot.start_datetime = arrow.utcnow().datetime
    slot.end_datetime = arrow.utcnow().shift(days=10).datetime
    assert manager.get_overlapping_entries(slot).count()


def test_availability_slot_manager_get_get_between_dates(
        availability_slots: QuerySet):
    """Should return slots between the dates."""
    professional = availability_slots.first().professional
    service = availability_slots.exclude(service__isnull=True).first().service
    manager: AvailabilitySlotManager = AvailabilitySlot.objects
    start = arrow.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    end = start.shift(days=10)

    result = manager.get_between_dates(start, end, professional)
    assert result.count() == 10
    assert result.first().professional == professional

    result = manager.get_between_dates(
        start,
        end,
        service.professional,
        service,
    )
    assert result.count() == 10
    assert result.first().service == service

    end = start.shift(days=100)
    result = manager.get_between_dates(start, end, professional)
    assert result.count() == 61


def test_professional_closed_period_manager_get_get_between_dates(
        professional_closed_periods: QuerySet):
    """Should return slots between the dates."""
    professional = professional_closed_periods.first().professional
    manager = ProfessionalClosedPeriod.objects
    start = arrow.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    end = start.shift(days=10)

    result = manager.get_between_dates(start, end, professional)
    assert result.count() == 2
    assert result.first().professional == professional

    assert manager.get_between_dates(
        start.shift(days=6),
        start.shift(days=15),
        professional,
    ).count() == 1

    assert manager.get_between_dates(
        start.shift(days=20),
        start.shift(days=30),
        professional,
    ).count() == 0


def test_service_closed_period_manager_get_get_between_dates(
        service_closed_periods: QuerySet):
    """Should return slots between the dates."""
    service = service_closed_periods.first().service
    manager = ServiceClosedPeriod.objects
    start = arrow.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    end = start.shift(days=10)

    result = manager.get_between_dates(start, end, service)
    assert result.count() == 2
    assert result.first().service == service

    assert manager.get_between_dates(
        start.shift(days=6),
        start.shift(days=15),
        service,
    ).count() == 1

    assert manager.get_between_dates(
        start.shift(days=20),
        start.shift(days=30),
        service,
    ).count() == 0
