"""The search engine validators module."""

from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError

from d8b.validators import validate_datetime_in_future

from .exceptions import SearchValidationError

if TYPE_CHECKING:
    from .request import (SearchLocationRequest, SearchProfessionalRequest,
                          SearchRequest, SearchServiceRequest)


def validate_search_request_dates(request: "SearchRequest"):
    """Validate the calendar request dates."""
    start = request.start_datetime
    end = request.end_datetime
    try:
        if start:
            validate_datetime_in_future(start)
        if end:
            validate_datetime_in_future(end)
    except ValidationError as error:
        raise SearchValidationError(str(error)) from error
    if start and end and start >= end:
        raise SearchValidationError(
            "Start datetime is greater or equal than the end datetime.")


def validate_search_request_location(request: "SearchLocationRequest"):
    """Validate the calendar request location."""
    if request.max_distance is not None and request.max_distance < 1:
        raise SearchValidationError(
            "The maximum distance must be greater than 1")


def validate_search_request_professional(request: "SearchProfessionalRequest"):
    """Validate the calendar request professional."""
    if request.rating and request.rating < 0:
        raise SearchValidationError("The rating must be greater than 0")
    if request.experience and request.experience < 0:
        raise SearchValidationError("The experience must be greater than 0")
    if request.start_age and request.end_age and \
            request.start_age >= request.end_age:
        raise SearchValidationError(
            "Start age is greater or equal than the end age.")


def validate_search_request_service(request: "SearchServiceRequest"):
    """Validate the calendar request service."""
    start_price = request.start_price
    end_price = request.end_price

    if start_price and start_price.amount <= 0:
        raise SearchValidationError("The start price must be greater than 0")
    if end_price and end_price.amount <= 0:
        raise SearchValidationError("The end price must be greater than 0")
    try:
        if start_price and end_price and start_price > end_price:
            raise SearchValidationError(
                "Start price is greater than the end price.")
    except TypeError as error:
        raise SearchValidationError("The prices are invalid") from error


def validate_search_request(request: "SearchRequest"):
    """Validate the calendar request."""
    validate_search_request_dates(request)
    validate_search_request_location(request.location)
    validate_search_request_professional(request.professional)
    validate_search_request_service(request.service)
