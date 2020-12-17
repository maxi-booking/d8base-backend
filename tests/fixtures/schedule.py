"""The schedule fixtures module."""

from datetime import time
from typing import List

import arrow
import pytest
from django.db.models.query import QuerySet
from pytest_mock.plugin import MockerFixture

from schedule.models import (AvailabilitySlot, ProfessionalClosedPeriod,
                             ProfessionalSchedule, ServiceClosedPeriod,
                             ServiceSchedule)

# pylint: disable=redefined-outer-name


@pytest.fixture
def disable_slots_signals(mocker: MockerFixture):
    """Disable the slots signals."""
    mocker.patch("orders.signals.generate_for_order")
    mocker.patch("schedule.signals.generate_for_service")
    mocker.patch("schedule.signals.generate_for_professional")


@pytest.fixture
def professional_schedules(professionals: QuerySet) -> QuerySet:
    """Return a professional schedule queryset."""
    for professional in professionals:
        for i in range(0, 5):
            ProfessionalSchedule.objects.create(
                professional=professional,
                day_of_week=i,
                start_time=time(9),
                end_time=time(14),
            )
            ProfessionalSchedule.objects.create(
                professional=professional,
                day_of_week=i,
                start_time=time(15),
                end_time=time(18),
            )
    return ProfessionalSchedule.objects.get_list()


@pytest.fixture
def service_schedules(services: QuerySet) -> QuerySet:
    """Return a service schedule queryset."""
    for service in services:
        for i in range(0, 5):
            ServiceSchedule.objects.create(
                service=service,
                day_of_week=i,
                start_time=time(9),
                end_time=time(14),
            )
            ServiceSchedule.objects.create(
                service=service,
                day_of_week=i,
                start_time=time(15),
                end_time=time(18),
            )

    return ServiceSchedule.objects.get_list()


@pytest.fixture
def professional_closed_periods(professionals: QuerySet) -> QuerySet:
    """Return a professional closed periods queryset."""
    for professional in professionals:
        ProfessionalClosedPeriod.objects.create(
            professional=professional,
            start_datetime=arrow.utcnow().shift(days=+2).datetime,
            end_datetime=arrow.utcnow().shift(days=+4).datetime,
        )
        ProfessionalClosedPeriod.objects.create(
            professional=professional,
            start_datetime=arrow.utcnow().shift(days=+5).datetime,
            end_datetime=arrow.utcnow().shift(days=+10).datetime,
        )
    return ProfessionalClosedPeriod.objects.get_list()


@pytest.fixture
def service_closed_periods(services: QuerySet) -> QuerySet:
    """Return a service closed periods queryset."""
    for service in services:
        ServiceClosedPeriod.objects.create(
            service=service,
            start_datetime=arrow.utcnow().shift(days=+2).datetime,
            end_datetime=arrow.utcnow().shift(days=+4).datetime,
        )
        ServiceClosedPeriod.objects.create(
            service=service,
            start_datetime=arrow.utcnow().shift(days=+5).datetime,
            end_datetime=arrow.utcnow().shift(days=+10).datetime,
        )
    return ServiceClosedPeriod.objects.get_list()


@pytest.fixture
def availability_slots(
    professionals: QuerySet,
    services: QuerySet,
) -> QuerySet:
    """Return a availability slots queryset."""
    slots: List[AvailabilitySlot] = []
    start = arrow.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    end = start.shift(days=60)
    for professional in professionals:
        for current in arrow.Arrow.range("day", start, end):
            slot = AvailabilitySlot()
            slot.professional = professional
            slot.start_datetime = current.replace(hour=9).datetime
            slot.end_datetime = current.replace(hour=17, minute=30).datetime
            slots.append(slot)

    for service in services:
        for current in arrow.Arrow.range("day", start, end):
            slot = AvailabilitySlot()
            slot.professional = service.professional
            slot.service = service
            slot.start_datetime = current.replace(hour=11).datetime
            slot.end_datetime = current.replace(hour=15).datetime
            slots.append(slot)

    AvailabilitySlot.objects.all().delete()
    AvailabilitySlot.objects.bulk_create(slots)

    return AvailabilitySlot.objects.get_list()
