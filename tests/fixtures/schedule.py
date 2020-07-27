"""The schedule fixtures module."""

from datetime import time

import arrow
import pytest
from django.db.models.query import QuerySet

from schedule.models import (ProfessionalClosedPeriod, ProfessionalSchedule,
                             ServiceClosedPeriod, ServiceSchedule)

# pylint: disable=redefined-outer-name


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
            start_datetime=arrow.utcnow().shift(days=+2).date(),
            end_datetime=arrow.utcnow().shift(days=+4).date(),
        )
        ProfessionalClosedPeriod.objects.create(
            professional=professional,
            start_datetime=arrow.utcnow().shift(days=+5).date(),
            end_datetime=arrow.utcnow().shift(days=+10).date(),
        )
    return ProfessionalClosedPeriod.objects.get_list()


@pytest.fixture
def service_closed_periods(services: QuerySet) -> QuerySet:
    """Return a service closed periods queryset."""
    for service in services:
        ServiceClosedPeriod.objects.create(
            service=service,
            start_datetime=arrow.utcnow().shift(days=+2).date(),
            end_datetime=arrow.utcnow().shift(days=+4).date(),
        )
        ServiceClosedPeriod.objects.create(
            service=service,
            start_datetime=arrow.utcnow().shift(days=+5).date(),
            end_datetime=arrow.utcnow().shift(days=+10).date(),
        )
    return ServiceClosedPeriod.objects.get_list()
