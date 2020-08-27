"""The calendar request test module."""
import pytest
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils import timezone
from pytest_mock.plugin import MockFixture
from rest_framework.request import Request

from schedule.calendar.request import (CalendarPeriod,
                                       HTTPToCalendarRequestConverter)

pytestmark = pytest.mark.django_db

# pylint: disable=protected-access


def test_http_to_calendar_request_converter(
    professionals: QuerySet,
    services: QuerySet,
    mocker: MockFixture,
):
    """Should convert a HTTP request to a calendar request."""
    tz_name = "America/New_York"
    datetime_format = "YYYY-MM-DDTHH:mm:ss"
    timezone.activate(tz_name)
    validator = mocker.MagicMock(return_value=None)
    professional = professionals.first()
    service = services.filter(professional=professional).first()
    request = HttpRequest()
    request.GET["professional"] = professional.pk
    request.GET["service"] = service.pk
    converter = HTTPToCalendarRequestConverter(Request(request))
    converter.validator = validator
    result = converter.get()

    assert result.professional == professional
    assert result.service == service
    assert validator.call_count == 1

    start_datetime = "2020-08-23T16:19:43"
    end_datetime = "2021-08-23T16:19:43"
    request.GET["start_datetime"] = start_datetime
    request.GET["end_datetime"] = end_datetime
    request.GET["period"] = "slot"

    result = HTTPToCalendarRequestConverter(Request(request)).get()

    assert result.start_datetime
    assert result.end_datetime
    assert result.start_datetime.utcoffset().total_seconds() == 0
    assert result.end_datetime.utcoffset().total_seconds() == 0
    assert start_datetime == result.start_datetime.to(tz_name).format(
        datetime_format)
    assert end_datetime == result.end_datetime.to(tz_name).format(
        datetime_format)
    assert result.period == CalendarPeriod.SLOT
