"""The commands test module."""
import pytest
from django.core.management import call_command
from django.db.models.query import QuerySet
from pytest_mock import MockFixture

pytestmark = pytest.mark.django_db


def test_generate_slots(
    professionals: QuerySet,
    services: QuerySet,
    mocker: MockFixture,
):
    """Should filter a queryset by user."""
    generator = mocker.MagicMock()
    get_generator = mocker.MagicMock(return_value=generator)
    mocker.patch(
        "schedule.availability.generator.get_availability_generator",
        new=get_generator,
    )
    call_command("generate_slots")
    total = professionals.count() + services.count()
    assert get_generator.called
    assert get_generator.call_count == total
    assert generator.generate.called
    assert generator.generate.call_count == total

    call_command(
        "generate_slots",
        professionals=[professionals.first().pk],
        services=[services.filter(is_base_schedule=True).first().pk],
    )
    assert generator.generate.call_count == total + 2
