"""The calendar request test module."""
import arrow
import pytest
from django.db.models.query import QuerySet
from pytest_mock import MockFixture

from schedule.calendar.generator import (CalendarGenerator,
                                         get_calendar_generator)
from schedule.calendar.request import CalendarRequest

pytestmark = pytest.mark.django_db

# pylint: disable=protected-access


def test_get_calendar_generator():
    """Should return an instance of the calendar generator."""
    generator = get_calendar_generator()
    assert isinstance(generator, CalendarGenerator)


def test_get_calendar_generator_get(
    professionals: QuerySet,
    mocker: MockFixture,
):
    """Should return an instance of the calendar generator."""
    request = CalendarRequest()
    request.professional = professionals.first()
    request.start_datetime = arrow.utcnow()
    request.end_datetime = arrow.utcnow().shift(days=7)
    generator = get_calendar_generator()
    mock = mocker.MagicMock(return_value=[])
    generator._manager.get_between_dates = mock

    generator.get(request)
    mock.assert_called_once_with(
        professional=request.professional,
        service=request.service,
        start=request.start_datetime,
        end=request.end_datetime,
    )
