"""The availability generator module."""
import logging
from abc import ABC, abstractmethod
from typing import DefaultDict, List, Optional, TypeVar

import arrow
from django.conf import settings

from schedule.models import (AvailabilitySlot, ProfessionalSchedule, Schedule,
                             ServiceSchedule)
from services.models import Service

from .db import AbstractSaver, DeleteSaver
from .exceptions import AvailabilityError, AvailabilityValueError
from .request import (AbstractRequestProcessor, Request,
                      RequestAppendProcessor, RequestYearProcessor)
from .restrictions import AbstractRestriction, ClosedPeriodsRestriction

T = TypeVar("T", bound="AbstractGenerator")


class AbstractGenerator(ABC):
    """The abstract generator."""

    _request: Request
    _service: Optional[Service] = None

    def set_request(self: T, request: Request) -> T:
        """Set a  request."""
        self._request = request
        self._set_service()
        return self

    def _set_service(self) -> None:
        """Set the service."""
        self._service = None
        if self._request.service and not\
                self._request.service.is_base_schedule:
            self._service = self._request.service

    def _check_request(self):
        """Check if the request is set."""
        if not getattr(self, "_request", None):
            raise AvailabilityValueError("The request is not set.")

    @abstractmethod
    def _get(self) -> List[AvailabilitySlot]:
        """Generate and return availability slots."""

    def get(self) -> List[AvailabilitySlot]:
        """Generate and return availability slots."""
        self._check_request()
        return self._get()


class DefaultGenerator(AbstractGenerator):
    """The default generator."""

    def _get_schedules(self) -> DefaultDict[int, List[Schedule]]:
        """Get the schedules."""
        if self._service:
            return ServiceSchedule.objects.get_by_days(self._service)

        return ProfessionalSchedule.objects.get_by_days(
            self._request.professional)

    @staticmethod
    def _combine_adjacent_slots(
            slots: List[AvailabilitySlot]) -> List[AvailabilitySlot]:
        """Combine adjacent slots."""
        i = 1
        while i < len(slots):
            prev = slots[i - 1]
            current = slots[i]
            diff = (current.start_datetime - prev.end_datetime).total_seconds()
            if diff <= settings.AVAILABILITY_MIN_SLOT_DIFF_TO_COMBINE:
                current.start_datetime = prev.start_datetime
                del slots[i - 1]
            i += 1

        return slots

    def _get(self) -> List[AvailabilitySlot]:
        """Generate and return availability slots."""
        schedules = self._get_schedules()
        slots: List[AvailabilitySlot] = []
        interval = arrow.Arrow.range(
            "day",
            self._request.start_datetime,
            self._request.end_datetime,
        )
        self._set_service()

        for current in interval:
            for schedule in schedules[current.weekday()]:
                slot = AvailabilitySlot()
                slot.professional = self._request.professional
                if self._service:
                    slot.service = self._service
                slot.start_datetime = current.replace(
                    tzinfo=schedule.timezone,
                    hour=schedule.start_time.hour,
                    minute=schedule.start_time.minute,
                ).to("UTC").datetime
                slot.end_datetime = current.replace(
                    tzinfo=schedule.timezone,
                    hour=schedule.end_time.hour,
                    minute=schedule.end_time.minute,
                ).to("UTC").datetime
                slots.append(slot)
        return self._combine_adjacent_slots(slots)


class AvailabilityGenerator():
    """The availability generator."""

    request: Request
    generator: AbstractGenerator = DefaultGenerator()
    saver: AbstractSaver = DeleteSaver()
    request_processor: AbstractRequestProcessor
    logger: logging.Logger
    restrictions: List[AbstractRestriction] = [ClosedPeriodsRestriction()]

    def __init__(self, request: Request):
        """Construct the object."""
        self.request = request

    def _apply_restrictions(
        self,
        slots: List[AvailabilitySlot],
    ) -> List[AvailabilitySlot]:
        """Apply the restrictions."""
        for restriction in self.restrictions:
            slots = restriction.set_request(self.request).\
                set_slots(slots).apply()
        return slots

    def generate(self) -> None:
        """Generate the availability slots."""
        try:
            self.request = self.request_processor.get(self.request)
            slots = self.generator.set_request(self.request).get()
            slots = self._apply_restrictions(slots)
            self.saver.set_request(self.request).set_slots(slots).save()
            self.logger.info(
                "AvailabilityGenerator report: request %s",
                self.request,
            )
        except AvailabilityError as error:
            self.logger.error(
                "AvailabilityGenerator error: %s; request %s",
                error,
                self.request,
            )


def get_availability_generator(request: Request) -> AvailabilityGenerator:
    """Return the availability generator."""
    generator = AvailabilityGenerator(request)
    generator.logger = logging.getLogger("d8b")
    generator.request_processor = RequestYearProcessor()
    if request.append_days:
        generator.request_processor = RequestAppendProcessor()
    return generator
