"""The calendar validators test module."""
import arrow
import pytest
from django.db.models.query import QuerySet

from schedule.calendar import validators
from schedule.calendar.exceptions import CalendarValidationError
from schedule.calendar.request import CalendarRequest

pytestmark = pytest.mark.django_db

# pylint: disable=protected-access


def test_validate_calendar_not_empty():
    """Should check if a value is not empty."""
    request = CalendarRequest()
    with pytest.raises(CalendarValidationError) as error:
        validators._validate_calendar_not_empty(request, "start_datetime")
    assert "start_datetime" in str(error)

    request.start_datetime = "test"
    validators._validate_calendar_not_empty(request, "start_datetime")


def test_validate_calendar_isinstance():
    """Should check if a value is instance of the provided class."""
    with pytest.raises(CalendarValidationError) as error:
        validators._validate_calendar_isinstance("str", int, "test title")
    assert "test title" in str(error)

    validators._validate_calendar_isinstance("value", str, "test title")


def test_validate_calendar_datetime():
    """Should validate the request datetime."""
    with pytest.raises(CalendarValidationError) as error:
        validators._validate_calendar_datetime("str", "test title")
    assert "test title" in str(error)

    with pytest.raises(CalendarValidationError) as error:
        validators._validate_calendar_datetime(
            arrow.now("US/Pacific"),
            "test title",
        )
    assert "test title" in str(error)

    validators._validate_calendar_datetime(arrow.utcnow(), "test title")


def test_calendar_validate_request(
    professionals: QuerySet,
    services: QuerySet,
):
    """Should validate a calendar request."""
    request = CalendarRequest()
    professional = professionals.first()
    request.professional = professional
    start = arrow.utcnow()
    end = start.shift(hours=-1)
    request.start_datetime = start
    request.end_datetime = end

    with pytest.raises(CalendarValidationError) as error:
        validators.validate_calendar_request(request)
    assert "start datetime" in str(error)
    assert "end datetime" in str(error)

    end = start.shift(hours=1)
    request.end_datetime = end
    validators.validate_calendar_request(request)

    service = services.exclude(professional=professional).first()
    request.service = service

    with pytest.raises(CalendarValidationError) as error:
        validators.validate_calendar_request(request)
    assert "service" in str(error)

    request.service = request.professional.services.first()  # type: ignore
    validators.validate_calendar_request(request)
