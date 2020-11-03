"""The availability request test module."""
import pytest
from django.db.models.query import QuerySet
from pytest_mock import MockFixture

from schedule.availability.tasks import (
    generate_future_availability_slots_task,
    remove_expired_availability_slots_task)

pytestmark = pytest.mark.django_db


def test_remove_expired_availability_slots_task(mocker: MockFixture):
    """Should run the delete_expired_availability_slots."""
    mock = mocker.patch(
        "schedule.availability.tasks.delete_expired_availability_slots")
    remove_expired_availability_slots_task.apply_async()

    assert mock.called


def test_generate_future_availability_slots_task(
    professionals: QuerySet,
    services: QuerySet,
    mocker: MockFixture,
):
    """Should generate future availability slots."""
    professionals_generator = mocker.patch(
        "schedule.availability.tasks.generate_for_professional")
    services_generator = mocker.patch(
        "schedule.availability.tasks.generate_for_service")
    generate_future_availability_slots_task.apply_async()

    assert professionals_generator.call_count == professionals.count()
    assert services_generator.call_count == services.filter(
        is_base_schedule=False).count()

    professionals_generator.assert_called_with(
        professionals.last(),
        append_days=True,
    )
    services_generator.assert_called_with(
        services.filter(is_base_schedule=False).last(),
        append_days=True,
    )
