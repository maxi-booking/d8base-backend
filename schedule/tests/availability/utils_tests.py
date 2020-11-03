"""The availability request test module."""
import arrow
import pytest
from django.db.models.query import QuerySet
from pytest_mock import MockFixture

from schedule.availability.utils import (delete_expired_availability_slots,
                                         generate_for_professional,
                                         generate_for_service)

pytestmark = pytest.mark.django_db


def test_generate_for_professional(
    professionals: QuerySet,
    mocker: MockFixture,
):
    """Should run the generator."""
    professional = professionals.first()
    start = arrow.utcnow()
    end = start.shift(days=1)
    generator = mocker.MagicMock()
    get_generator = mocker.MagicMock(return_value=generator)
    mocker.patch(
        "schedule.availability.utils.get_availability_generator",
        new=get_generator,
    )
    generate_for_professional(
        professional=professional,
        append_days=True,
        start=start,
        end=end,
    )
    get_generator.assert_called_once()
    generator.generate.assert_called_once()

    request = get_generator.call_args_list[0][0][0]

    assert request.professional == professional
    assert request.start_datetime == start
    assert request.end_datetime == end
    assert request.append_days is True


def test_generate_for_service(
    services: QuerySet,
    mocker: MockFixture,
):
    """Should run the generator."""
    service = services.first()
    start = arrow.utcnow()
    end = start.shift(days=1)
    generator = mocker.MagicMock()
    get_generator = mocker.MagicMock(return_value=generator)
    mocker.patch(
        "schedule.availability.utils.get_availability_generator",
        new=get_generator,
    )
    generate_for_service(
        service=service,
        append_days=True,
        start=start,
        end=end,
    )
    get_generator.assert_called_once()
    generator.generate.assert_called_once()

    request = get_generator.call_args_list[0][0][0]

    assert request.service == service
    assert request.professional == service.professional
    assert request.start_datetime == start
    assert request.end_datetime == end
    assert request.append_days is True


def test_delete_expired_availability_slots(availability_slots: QuerySet):
    """Should delete the expired availability slots."""
    yesterday = arrow.utcnow().shift(days=-2).datetime
    today = arrow.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    ).datetime
    professional_schedule = availability_slots.filter(
        service__isnull=True).first()
    professional_schedule.end_datetime = yesterday
    professional_schedule.save()

    service_schedule = availability_slots.filter(service__isnull=False).first()
    service_schedule.end_datetime = yesterday
    service_schedule.save()

    assert availability_slots.filter(end_datetime__lt=today).count() == 2

    delete_expired_availability_slots()
    assert availability_slots.filter(end_datetime__lt=today).count() == 0
