"""The calendar request test module."""
import arrow
import pytest
from django.db.models.query import QuerySet
from django.utils.timezone import get_current_timezone

from schedule.calendar.exceptions import CalendarValueError
from schedule.calendar.generator import CalendarPeriodGenerator
from schedule.calendar.request import CalendarPeriod, CalendarRequest
from services.models import Service

pytestmark = pytest.mark.django_db

# pylint: disable=protected-access


def test_calendar_period_generator_set_request():
    """Should set the request."""
    with pytest.raises(CalendarValueError) as error:
        generator = CalendarPeriodGenerator()
        generator.get()
    assert "request is not set" in str(error)
    request = CalendarRequest()
    request.start_datetime = arrow.utcnow()
    request.end_datetime = arrow.utcnow()
    generator.set_request(request).get()


def test_calendar_period_generator_get_slot(
    professionals: QuerySet,
    services: QuerySet,
):
    # pylint: disable=unused-argument
    """Should return the generated calendar respone periods."""
    professional = professionals.first()
    request = CalendarRequest()
    request.professional = professional
    duration = Service.objects.get_min_duration(professional)
    request.start_datetime = arrow.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    request.end_datetime = request.start_datetime.shift(days=1)
    request.period = CalendarPeriod.SLOT

    generator = CalendarPeriodGenerator()
    result = generator.set_request(request).get()
    assert len(result) == 24

    assert result[0].timezone == get_current_timezone()
    assert not result[0].is_open
    assert result[0].period_start == request.start_datetime
    assert result[0].period_end == request.start_datetime.shift(
        minutes=duration)

    assert result[1].period_start == request.start_datetime.shift(
        minutes=duration)
    assert result[1].period_end == request.start_datetime.shift(
        minutes=duration * 2)

    assert result[-1].period_start == request.end_datetime.shift(
        minutes=-duration)
    assert result[-1].period_end == request.end_datetime.shift()


def test_calendar_period_generator_get_day(professionals: QuerySet):
    """Should return the generated calendar respone periods."""
    professional = professionals.first()
    request = CalendarRequest()
    request.professional = professional
    request.start_datetime = arrow.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    request.end_datetime = request.start_datetime.shift(months=1)
    request.period = CalendarPeriod.DAY

    generator = CalendarPeriodGenerator()
    result = generator.set_request(request).get()
    assert len(result) == (request.end_datetime - request.start_datetime).days

    assert result[0].timezone == get_current_timezone()
    assert not result[0].is_open
    assert result[0].period_start == request.start_datetime
    assert result[0].period_end == request.start_datetime.shift(days=1)

    assert result[1].period_start == request.start_datetime.shift(days=1)
    assert result[1].period_end == request.start_datetime.shift(days=2)

    assert result[-1].period_start == request.end_datetime.shift(days=-1)
    assert result[-1].period_end == request.end_datetime.shift()
