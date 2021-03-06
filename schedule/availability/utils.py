"""The availability utils module."""

from typing import TYPE_CHECKING, Optional

import arrow

from d8b.lock import distributed_lock
from schedule.models import AvailabilitySlot

from .generator import get_availability_generator
from .request import Request

if TYPE_CHECKING:
    from orders.models import Order
    from professionals.models import Professional
    from services.models import Service


def delete_expired_availability_slots():
    """Delete expired availability slots."""
    AvailabilitySlot.objects.get_expired_entries().delete()


@distributed_lock(
    prefix="generate_for_professional",
    keys=["professional"],
    timeout=60 * 5,
)
def generate_for_professional(
    *,
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


@distributed_lock(
    prefix="generate_for_professional",
    keys=["service"],
    timeout=60 * 5,
)
def generate_for_service(
    *,
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


def generate_for_order(order: "Order"):
    """Generate slots form the order for the year."""
    generate_for_professional(professional=order.service.professional)
    if not order.service.is_base_schedule:
        generate_for_service(service=order.service)
