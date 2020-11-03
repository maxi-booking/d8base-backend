"""The availability utils module."""

from typing import TYPE_CHECKING, Optional

import arrow

from schedule.models import AvailabilitySlot

from .generator import get_availability_generator
from .request import Request

if TYPE_CHECKING:
    from professionals.models import Professional
    from services.models import Service


def delete_expired_availability_slots():
    """Delete expired availability slots."""
    AvailabilitySlot.objects.get_expired_entries().delete()


def generate_for_professional(
    professional: "Professional",
    append_days: bool = False,
    start: Optional[arrow.Arrow] = None,
    end: Optional[arrow.Arrow] = None,
):
    """Generate slots form the professional for the year."""
    request = Request()
    request.start_datetime = start
    request.end_datetime = end
    request.professional = professional
    request.append_days = append_days
    get_availability_generator(request).generate()


def generate_for_service(
    service: "Service",
    append_days: bool = False,
    start: Optional[arrow.Arrow] = None,
    end: Optional[arrow.Arrow] = None,
):
    """Generate slots form the professional for the year."""
    request = Request()
    request.start_datetime = start
    request.end_datetime = end
    request.professional = service.professional
    request.service = service
    request.append_days = append_days
    get_availability_generator(request).generate()
