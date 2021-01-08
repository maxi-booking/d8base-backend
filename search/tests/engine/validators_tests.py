"""The search engine request tests module."""

from unittest.mock import call

import arrow
import pytest
from django.core.exceptions import ValidationError
from djmoney.money import Money
from pytest_mock import MockFixture

from search.engine import validators
from search.engine.exceptions import SearchValidationError
from search.engine.request import SearchRequest

pytestmark = pytest.mark.django_db

# pylint: disable=protected-access


def test_validate_search_request_dates(mocker: MockFixture):
    """Should validate the request dates."""
    future = mocker.patch(
        "search.engine.validators.validate_datetime_in_future")
    request = SearchRequest()
    request.start_datetime = arrow.utcnow().shift(months=1)
    request.end_datetime = arrow.utcnow()

    with pytest.raises(SearchValidationError) as error:
        validators.validate_search_request_dates(request)

    assert "is greater or equal than the end datetime." in str(error)
    future.assert_has_calls([
        call(request.start_datetime),
        call(request.end_datetime),
    ])

    request.start_datetime = arrow.utcnow()
    request.end_datetime = arrow.utcnow().shift(months=1)
    validators.validate_search_request_dates(request)

    mocker.patch(
        "search.engine.validators.validate_datetime_in_future",
        side_effect=ValidationError("test exception"),
    )
    with pytest.raises(SearchValidationError) as error:
        validators.validate_search_request_dates(request)
    assert "test exception" in str(error)


def test_validate_search_request_location():
    """Should validate the location."""
    request = SearchRequest()
    request.location.max_distance = -1

    with pytest.raises(SearchValidationError) as error:
        validators.validate_search_request_location(request.location)
    assert "must be greater than 1" in str(error)

    request.location.max_distance = 2
    validators.validate_search_request_location(request.location)


def test_validate_search_request_professional():
    """Should validate the professional."""
    request = SearchRequest()
    request.professional.rating = -1

    with pytest.raises(SearchValidationError) as error:
        validators.validate_search_request_professional(request.professional)
    assert "rating must be greater than 0" in str(error)

    request.professional.rating = 2
    request.professional.experience = -1
    with pytest.raises(SearchValidationError) as error:
        validators.validate_search_request_professional(request.professional)
    assert "experience must be greater than 0" in str(error)

    request.professional.rating = 2
    request.professional.experience = 3
    request.professional.start_age = 15
    request.professional.end_age = 5

    with pytest.raises(SearchValidationError) as error:
        validators.validate_search_request_professional(request.professional)
    assert "Start age is greater or equal than the end age" in str(error)

    request.professional.rating = 2
    request.professional.experience = 3
    request.professional.start_age = 15
    request.professional.end_age = 25
    validators.validate_search_request_professional(request.professional)


def test_validate_search_request_service():
    """Should validate the service."""
    request = SearchRequest()
    request.service.start_price = Money(-1, "EUR")

    with pytest.raises(SearchValidationError) as error:
        validators.validate_search_request_service(request.service)
    assert "start price must be greater than 0" in str(error)

    request.service.start_price = Money(15, "EUR")
    request.service.end_price = Money(-1, "EUR")
    with pytest.raises(SearchValidationError) as error:
        validators.validate_search_request_service(request.service)
    assert "end price must be greater than 0" in str(error)

    request.service.start_price = Money(15, "EUR")
    request.service.end_price = Money(5, "EUR")

    with pytest.raises(SearchValidationError) as error:
        validators.validate_search_request_service(request.service)
    assert "Start price is greater than the end price" in str(error)

    request.service.start_price = Money(15, "USD")
    request.service.end_price = Money(5, "EUR")

    with pytest.raises(SearchValidationError) as error:
        validators.validate_search_request_service(request.service)
    assert "invalid" in str(error)

    request.service.start_price = Money(5, "EUR")
    request.service.end_price = Money(15, "EUR")
    validators.validate_search_request_service(request.service)


def test_validate_search_request(mocker: MockFixture):
    """Should validate the search request."""
    dates = mocker.patch(
        "search.engine.validators.validate_search_request_dates")
    location = mocker.patch(
        "search.engine.validators.validate_search_request_location")
    professional = mocker.patch(
        "search.engine.validators.validate_search_request_professional")
    service = mocker.patch(
        "search.engine.validators.validate_search_request_service")
    request = SearchRequest()
    validators.validate_search_request(request)

    dates.assert_called_once_with(request)
    location.assert_called_once_with(request.location)
    professional.assert_called_once_with(request.professional)
    service.assert_called_once_with(request.service)
