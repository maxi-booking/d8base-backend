"""The d8b validators tests module."""
import arrow
import pytest
from django.core.exceptions import ValidationError

from d8b.interfaces import StartEndDateEntry
from d8b.validators import (validate_date_in_past, validate_datetime_in_future,
                            validate_start_end_dates)


def test_validate_datetime_in_future():
    """Should raise an error if the datetime is not in the future."""
    future_date = arrow.utcnow().shift(days=1).datetime
    past_date = arrow.utcnow().shift(days=-1).datetime

    with pytest.raises(ValidationError):
        validate_datetime_in_future(past_date)
    validate_datetime_in_future(future_date)


def test_validate_date_in_past():
    """Should raise an error if the date is not in the past."""
    future_date = arrow.utcnow().shift(days=1).date()
    past_date = arrow.utcnow().shift(days=-1).date()

    with pytest.raises(ValidationError):
        validate_date_in_past(future_date)
    validate_date_in_past(past_date)


def test_validate_star_end_dates():
    """Should raise an error if the start date is greater than the end date."""
    obj = StartEndDateEntry()
    obj.start_date = arrow.utcnow().shift(days=-2).date()
    obj.end_date = arrow.utcnow().shift(days=-3).date()

    with pytest.raises(ValidationError):
        validate_start_end_dates(obj)

    obj.start_date = arrow.utcnow().shift(days=-4).date()
    obj.is_still_here = True

    with pytest.raises(ValidationError):
        validate_start_end_dates(obj)

    obj.end_date = None
    validate_start_end_dates(obj)
