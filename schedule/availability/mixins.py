"""The availability mixins module."""

from typing import List, TypeVar

from schedule.models import AvailabilitySlot

from .exceptions import AvailabilityValueError
from .request import Request

T = TypeVar("T", bound="RequestSlotsSetterMixin")


class RequestSlotsSetterMixin():
    """The a request and slots setter mixin."""

    _request: Request
    _slots: List[AvailabilitySlot]

    def set_request(self: T, request: Request) -> T:
        """Set a request."""
        self._request = request
        return self

    def set_slots(self: T, slots: List[AvailabilitySlot]) -> T:
        """Set slots."""
        self._slots = slots
        return self

    def _check_request(self):
        """Check if the request is set."""
        if not getattr(self, "_request", None):
            raise AvailabilityValueError("The request is not set.")
        if getattr(self, "_slots", None) is None:
            raise AvailabilityValueError("The slots are not set.")
