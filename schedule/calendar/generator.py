"""The calendar generator module."""
from typing import Tuple

from schedule.managers import AvailabilitySlotManager
from schedule.models import AvailabilitySlot

from .request import CalendarRequest


class CalendarGenerator():
    """The calendar generator."""

    _manager: AvailabilitySlotManager = AvailabilitySlot.objects

    def get(self, request: CalendarRequest) -> Tuple[AvailabilitySlot, ...]:
        """Return the generated response."""
        response = self._manager.get_between_dates(
            professional=request.professional,
            service=request.service,
            start=request.start_datetime,
            end=request.end_datetime,
        )
        return tuple(response)


def get_calendar_generator():
    """Return the calendar generator."""
    return CalendarGenerator()
