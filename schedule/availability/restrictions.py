"""The restrictions db module."""

from abc import ABC, abstractmethod
from copy import deepcopy
from typing import List, Optional

from schedule.models import (AbstractPeriod, AvailabilitySlot, ClosedPeriod,
                             ProfessionalClosedPeriod, ServiceClosedPeriod)

from .mixins import RequestSlotsSetterMixin


class AbstractSlotsModifier(ABC):
    """The abstract slots modifier."""

    @abstractmethod
    def get_processed_slots(
        self,
        slots: List[AvailabilitySlot],
        period: AbstractPeriod,
    ) -> List[AvailabilitySlot]:
        """Return the processed slots."""


class SlotsModifier(AbstractSlotsModifier):
    """The default slots modifier."""

    def get_processed_slots(
        self,
        slots: List[AvailabilitySlot],
        period: AbstractPeriod,
    ) -> List[AvailabilitySlot]:
        """Check the slot against the period."""
        processed_slots: List[AvailabilitySlot] = []
        for slot in slots:
            # the period overlaps the entire slot
            if period.start_datetime <= slot.start_datetime and \
                    period.end_datetime >= slot.end_datetime:
                continue

            # the period overlaps with the slot
            if slot.start_datetime <= period.start_datetime <=\
                    slot.end_datetime or slot.start_datetime <= \
                    period.end_datetime <= slot.end_datetime:

                # cut off the tail of the slot
                if period.start_datetime <= slot.start_datetime:
                    slot.start_datetime = period.end_datetime
                    processed_slots.append(slot)

                # cut off the head of the slot
                elif period.end_datetime >= slot.end_datetime:
                    slot.end_datetime = period.start_datetime
                    processed_slots.append(slot)

                # split the slot into two slots
                else:
                    tail = deepcopy(slot)
                    tail.pk = None
                    tail.end_datetime = period.start_datetime
                    processed_slots.append(tail)

                    head = deepcopy(slot)
                    head.pk = None
                    head.start_datetime = period.end_datetime
                    processed_slots.append(head)

            # the period doesn't overlap with the slot
            else:
                processed_slots.append(slot)
        return processed_slots


class AbstractRestriction(ABC, RequestSlotsSetterMixin):
    """The abstract restriction."""

    _slots_modifier: AbstractSlotsModifier = SlotsModifier()

    @abstractmethod
    def _apply(self) -> List[AvailabilitySlot]:
        """Apply the restriction to the availability slots."""

    def apply(self) -> List[AvailabilitySlot]:
        """Apply the restriction to the availability slots."""
        self._check_request()
        if not self._slots:
            return []
        return self._apply()


class ClosedPeriodsRestriction(AbstractRestriction):
    """The closed period restriction."""

    professionals_periods: Optional[List[ClosedPeriod]] = None
    service_periods: Optional[List[ClosedPeriod]] = None

    def _get_closed_periods_for_slot(
        self,
        slot: AvailabilitySlot,
    ) -> List[ClosedPeriod]:
        """Get the closed periods for the provided slot."""
        if slot.service and not slot.service.is_base_schedule:
            if self.service_periods is None:
                self.service_periods = list(
                    ServiceClosedPeriod.objects.get_between_dates(
                        self._request.start_datetime,
                        self._request.end_datetime,
                        slot.service,
                    ))
            periods = self.service_periods
        else:
            if self.professionals_periods is None:
                self.professionals_periods = list(
                    ProfessionalClosedPeriod.objects.get_between_dates(
                        self._request.start_datetime,
                        self._request.end_datetime,
                        slot.professional,
                    ))
            periods = self.professionals_periods
        return periods

    def _apply(self) -> List[AvailabilitySlot]:
        """Apply the restriction to the availability slots."""
        processed_slots: List[AvailabilitySlot] = []
        self.professionals_periods = None
        self.service_periods = None

        for slot in self._slots:
            slots = [slot]
            for period in self._get_closed_periods_for_slot(slot):
                slots = self._slots_modifier.get_processed_slots(slots, period)
            processed_slots.extend(slots)
        return processed_slots
