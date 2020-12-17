"""The availability db module."""

from abc import ABC, abstractmethod

from django.db import transaction

from schedule.models import AvailabilitySlot

from .mixins import RequestSlotsSetterMixin


class AbstractSaver(ABC, RequestSlotsSetterMixin):
    """The abstract saver."""

    @abstractmethod
    def _save(self) -> None:
        """Save the availability slots."""

    def save(self) -> None:
        """Save the availability slots."""
        self._check_request()
        return self._save()


class DeleteSaver(AbstractSaver):
    """The saver."""

    def _delete_old_entries(self) -> None:
        """Delete the old entries before saving the new ones."""
        AvailabilitySlot.objects.get_between_dates(
            professional=self._request.professional,
            service=self._request.service,
            start=self._request.start_datetime,
            end=self._request.end_datetime.shift(days=1),  # type: ignore
        ).delete()

    def _save(self):
        """Save the availability slots."""
        with transaction.atomic():
            self._delete_old_entries()
            AvailabilitySlot.objects.bulk_create(self._slots)
