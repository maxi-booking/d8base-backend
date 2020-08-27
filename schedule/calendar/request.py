"""The calendar request module."""
from typing import Optional

import arrow
from django.utils.timezone import get_current_timezone
from rest_framework.request import Request

from d8b.enum import Enum
from professionals.models import Professional
from services.models import Service

from .validators import validate_calendar_request


class CalendarPeriod(Enum):
    """The calendar period class."""

    DAY: str = "day"
    SLOT: str = "slot"


class CalendarRequest():
    """The calendar request class."""

    professional: Professional
    service: Optional[Service] = None
    period: CalendarPeriod = CalendarPeriod.DAY
    start_datetime: arrow.Arrow
    end_datetime: arrow.Arrow


class HTTPToCalendarRequestConverter():
    """The http to calendar request converter class."""

    PROFESSIONAL_PARAM: str = "professional"
    SERVICE_PARAM: str = "service"
    PERIOD_PARAM: str = "period"
    START_DATETIME_PARAM: str = "start_datetime"
    END_DATETIME_PARAM: str = "end_datetime"

    request: Request
    calendar_request: CalendarRequest

    def __init__(self, request: Request):
        """Construct the object."""
        self.request = request
        self.validator = validate_calendar_request

    def _get_query_param(self, name: str) -> Optional[str]:
        """Get a param form the query params."""
        return self.request.query_params.get(name, None)

    def _set_professional(self):
        """Set a professional to the calendart request."""
        pk = self._get_query_param(self.PROFESSIONAL_PARAM)
        professional = Professional.objects.get_by_params(pk=pk)
        if professional:
            self.calendar_request.professional = professional

    def _set_service(self):
        """Set a service to the calendart request."""
        pk = self._get_query_param(self.SERVICE_PARAM)
        self.calendar_request.service = Service.objects.\
            get_by_params(pk=pk)

    def _set_period(self):
        """Set a period to the calendart request."""
        try:
            self.calendar_request.period = CalendarPeriod(
                self._get_query_param(self.PERIOD_PARAM))
        except ValueError:
            pass

    def _set_datetime(self, name: str):
        """Set a datetime to the calendart request."""
        date_str = str(self._get_query_param(name))
        try:
            date = arrow.get(date_str, tzinfo=get_current_timezone())
            setattr(self.calendar_request, name, date.to("utc"))
        except arrow.ParserError:
            pass

    def get(self) -> CalendarRequest:
        """Convert and return the HTTP request to a calendar request."""
        self.calendar_request = CalendarRequest()
        self._set_professional()
        self._set_service()
        self._set_period()
        self._set_datetime(self.START_DATETIME_PARAM)
        self._set_datetime(self.END_DATETIME_PARAM)
        self.validator(self.calendar_request)
        return self.calendar_request
