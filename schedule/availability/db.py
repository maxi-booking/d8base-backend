"""The availability db module."""

from abc import ABC, abstractmethod
from typing import List, TypeVar

from django.db import transaction

from schedule.models import AvailabilitySlot

from .exceptions import AvailabilityValueError
from .request import Request

T = TypeVar("T", bound="AbstractSaver")


class AbstractSaver(ABC):
    """The abstract saver."""

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

    @abstractmethod
    def _save(self) -> None:
        """Save the availability slots."""

    def save(self) -> None:
        """Save the availability slots."""
        self._check_request()
        if not self._slots:
            return None
        return self._save()


class DeleteSaver(AbstractSaver):
    """The saver."""

    def _delete_old_entries(self) -> None:
        """Delete the old entries before saving the new ones."""
        AvailabilitySlot.objects.get_between_dates(
            professional=self._slots[0].professional,
            service=self._slots[0].service,
            start=self._request.start_datetime,
            end=self._request.end_datetime.shift(days=1),  # type: ignore
        ).delete()

    def _save(self):
        """Save the availability slots."""
        with transaction.atomic():
            self._delete_old_entries()
            AvailabilitySlot.objects.bulk_create(self._slots)
