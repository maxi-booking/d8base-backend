"""The commands test module."""
import pytest
from django.core.management import call_command
from django.db.models.query import QuerySet
from pytest_mock import MockFixture

pytestmark = pytest.mark.django_db


def test_command_generate_slots(
    professionals: QuerySet,
    services: QuerySet,
    mocker: MockFixture,
):
    """Should filter a queryset by user."""
    professionals_generator = mocker.patch(
        "schedule.availability.generate_for_professional")
    services_generator = mocker.patch(
        "schedule.availability.generate_for_service")
    call_command("generate_slots")
    total_professionals = professionals.count()
    total_services = services.count()
    assert professionals_generator.call_count == total_professionals
    assert services_generator.call_count == total_services

    call_command(
        "generate_slots",
        professionals=[professionals.first().pk],
        services=[services.filter(is_base_schedule=False).first().pk],
    )
    assert professionals_generator.call_count == total_professionals + 1
    assert services_generator.call_count == total_services + 1
