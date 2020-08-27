"""The calendar validators module."""
from typing import TYPE_CHECKING, Any

import arrow

import schedule.calendar
from professionals.models import Professional
from services.models import Service

from .exceptions import CalendarValidationError

if TYPE_CHECKING:
    from .request import CalendarRequest


def _validate_calendar_datetime(value: Any, title: str):
    """Validate the calendar request datetime."""
    if not isinstance(
            value,
            arrow.Arrow,
    ) or value.utcoffset().total_seconds() != 0:
        raise CalendarValidationError(
            f"The request {title} datetime is invalid")


def _validate_calendar_not_empty(request: "CalendarRequest", title: str):
    """Check if the calendar request value is not empty."""
    if not getattr(request, title, None):
        raise CalendarValidationError(f"The request {title} is empty")


def _validate_calendar_isinstance(value: Any, expected: Any, title: str):
    """Check if the calendar request value is instance of the class."""
    if not value:
        return
    if not isinstance(value, expected):
        raise CalendarValidationError(f"The request {title} is invalid")


def validate_calendar_request(request: "CalendarRequest"):
    """Validate the calendar request."""
    _validate_calendar_not_empty(request, "professional")
    _validate_calendar_not_empty(request, "period")
    _validate_calendar_not_empty(request, "start_datetime")
    _validate_calendar_not_empty(request, "end_datetime")

    _validate_calendar_isinstance(request.professional, Professional,
                                  "professional")
    _validate_calendar_isinstance(request.service, Service, "service")
    _validate_calendar_isinstance(
        request.period,
        schedule.calendar.request.CalendarPeriod,
        "period",
    )

    _validate_calendar_datetime(request.start_datetime, "start")
    _validate_calendar_datetime(request.end_datetime, "end")

    if request.start_datetime >= request.end_datetime:  # type: ignore
        raise CalendarValidationError(
            "The start datetime must be less than the end datetime.")

    if request.service and \
            request.service.professional != request.professional:
        raise CalendarValidationError("The request service is invalid")
