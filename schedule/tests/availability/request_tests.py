"""The availability request test module."""

import arrow
import pytest
from django.conf import settings
from django.db.models.query import QuerySet

from schedule.availability.exceptions import AvailabilityValueError
from schedule.availability.request import (Request, RequestAppendProcessor,
                                           RequestValidator,
                                           RequestYearProcessor)

pytestmark = pytest.mark.django_db

# pylint: disable=protected-access


def test_abstract_request_processor_reset_date_to_midnight():
    """Should reset a dates to midnight."""
    processor = RequestYearProcessor()
    request = Request()
    request.start_datetime = arrow.utcnow().replace(hour=1)
    processor._request = request
    assert processor._reset_date_to_midnight("invalid") is None

    processor._reset_date_to_midnight("start_datetime")
    assert processor._request.start_datetime == arrow.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )


def test_availability_request_validator(
    professionals: QuerySet,
    services: QuerySet,
):
    """Should validate a request."""
    service = services.first()
    professional = professionals.exclude(pk=service.professional.pk).first()
    request = Request()
    now = arrow.utcnow()
    validator = RequestValidator()

    with pytest.raises(AvailabilityValueError) as error:
        validator.validate(request)
    assert "datetime is invalid" in str(error)

    request.start_datetime = now
    with pytest.raises(AvailabilityValueError) as error:
        validator.validate(request)
    assert "datetime is invalid" in str(error)

    request.end_datetime = request.start_datetime.shift(hours=-1)
    with pytest.raises(AvailabilityValueError) as error:
        validator.validate(request)
    assert "be less" in str(error)

    request.end_datetime = request.end_datetime.replace(tzinfo="Europe/London")
    with pytest.raises(AvailabilityValueError) as error:
        validator.validate(request)
    assert "datetime is invalid" in str(error)

    request.end_datetime = request.start_datetime.shift(months=1)
    with pytest.raises(AvailabilityValueError) as error:
        validator.validate(request)
    assert "professional is empty" in str(error)

    request.professional = professional
    request.service = service

    with pytest.raises(AvailabilityValueError) as error:
        validator.validate(request)
    assert "service is incorrect" in str(error)

    request.professional = service.professional
    validator.validate(request)


def test_availability_request_processor_custom_dates(professionals: QuerySet):
    """Should reset dates to midnight."""
    professional = professionals.first()
    request = Request()
    request.professional = professional
    start = arrow.utcnow()
    end = arrow.utcnow().shift()
    request.start_datetime = start
    request.end_datetime = end
    processor = RequestYearProcessor()
    new_request = processor.get(request)
    assert new_request.start_datetime == start.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    assert new_request.end_datetime == end.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )


def test_availability_request_year_processor(
    professionals: QuerySet,
    services: QuerySet,
):
    """Should set dates and a professional."""
    service = services.first()
    professional = professionals.exclude(pk=service.professional.pk).first()
    request = Request()
    request.service = service
    request.professional = professional
    processor = RequestYearProcessor()
    new_request = processor.get(request)
    assert new_request.professional == service.professional
    assert new_request.start_datetime == arrow.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    assert new_request.end_datetime == arrow.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    ).shift(years=1)


def test_availability_request_append_processor(
    professionals: QuerySet,
    services: QuerySet,
):
    """Should set dates and a professional."""
    service = services.first()
    professional = professionals.exclude(pk=service.professional.pk).first()
    request = Request()
    request.service = service
    request.professional = professional
    processor = RequestAppendProcessor()
    new_request = processor.get(request)
    assert new_request.professional == service.professional
    assert new_request.start_datetime == arrow.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    ).shift(years=1)
    assert new_request.end_datetime == new_request.start_datetime.shift(
        days=settings.AVAILABILITY_DAYS_TO_APPEND)
