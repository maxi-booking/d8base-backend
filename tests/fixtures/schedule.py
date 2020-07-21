"""The schedule fixtures module."""

from datetime import time

import pytest
from django.db.models.query import QuerySet

from schedule.models import ProfessionalSchedule, ServiceSchedule

# pylint: disable=redefined-outer-name


@pytest.fixture
def professional_schedules(professionals: QuerySet, ) -> QuerySet:
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
def service_schedules(services: QuerySet, ) -> QuerySet:
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
