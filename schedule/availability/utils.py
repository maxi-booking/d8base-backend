"""The availability utils module."""

from typing import TYPE_CHECKING, Optional

import arrow

from .generator import get_availability_generator
from .request import Request

if TYPE_CHECKING:
    from professionals.models import Professional
    from services.models import Service


def generate_for_professional(
    professional: "Professional",
    start: Optional[arrow.Arrow] = None,
    end: Optional[arrow.Arrow] = None,
):
    """Generate slots form the professional for the year."""
    request = Request()
    request.start_datetime = start
    request.end_datetime = end
    request.professional = professional
    get_availability_generator(request).generate()


def generate_for_service(
    service: "Service",
    start: Optional[arrow.Arrow] = None,
    end: Optional[arrow.Arrow] = None,
):
    """Generate slots form the professional for the year."""
    request = Request()
    request.start_datetime = start
    request.end_datetime = end
    request.professional = service.professional
    request.service = service
    get_availability_generator(request).generate()
