"""The calendar generator module."""
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, TypeVar

from django.utils.timezone import get_current_timezone

from services.models import Service

from .exceptions import CalendarValueError
from .request import CalendarPeriod, CalendarRequest
from .response import CalendarResponse

T = TypeVar("T", bound="AbstractPeriodGenerator")


class AbstractPeriodGenerator(ABC):
    """The abstract period generator."""

    _request: CalendarRequest

    def set_request(self: T, request: CalendarRequest) -> T:
        """Set a calendart request."""
        self._request = request
        return self

    @abstractmethod
    def get(self) -> List[CalendarResponse]:
        """Generate and return calendar responses."""


class CalendarPeriodGenerator(AbstractPeriodGenerator):
    """The abstract period generator."""

    def _get_min_slot(self) -> int:
        """Get the minimum datetime slot."""
        if self._request.service:
            return self._request.service.duration
        duration = Service.objects.get_min_duration(self._request.professional)
        if not duration:
            raise CalendarValueError("The min duration is empty")
        return duration

    def _get_period_shift(self) -> Dict[str, int]:
        """Get the period datetime shift."""
        if self._request.period == CalendarPeriod.DAY:
            return {"days": 1}
        return {"minutes": self._get_min_slot()}

    def _check_request(self):
        """Check if the request is set."""
        if not getattr(self, "_request", None):
            raise CalendarValueError("The request is not set.")

    def get(self) -> List[CalendarResponse]:
        """Generate and return calendar responses."""
        self._check_request()
        shift = self._get_period_shift()

        response = []
        timezone = get_current_timezone()

        current_start = self._request.start_datetime
        current_end = current_start.shift(**shift)
        while True:
            entry = CalendarResponse()
            entry.timezone = timezone
            entry.is_open = False
            entry.period_start = current_start
            entry.period_end = current_end
            response.append(entry)

            if current_end >= self._request.end_datetime:
                break

            current_start = current_end
            current_end = current_end.shift(**shift)

        return response


class CalendarGenerator():
    """The calendar generator."""

    periods_generator: AbstractPeriodGenerator = CalendarPeriodGenerator()

    # restrictions

    def get(self, request: CalendarRequest) -> Tuple[CalendarResponse, ...]:
        """Return the generated response."""
        response = self.periods_generator.set_request(request).get()
        return tuple(response)


def get_calendar_generator():
    """Return the calendar generator."""
    return CalendarGenerator()
