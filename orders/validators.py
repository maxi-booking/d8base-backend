"""The orders validators module."""
from datetime import datetime
from typing import TYPE_CHECKING

import arrow
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.translation import gettext_lazy as _

from d8b.validators import validate_datetime_in_future
from schedule.models import AvailabilitySlot

if TYPE_CHECKING:
    from .models import Order
    from services.models import Service


def validate_order_dates(order: "Order"):
    """Validate the order dates."""
    model = apps.get_model("orders", "Order")
    if not order.start_datetime or not order.end_datetime:
        raise ValidationError(_("The dates is not set"))
    if not order.pk:
        validate_datetime_in_future(order.start_datetime)
        validate_datetime_in_future(order.end_datetime)
    if order.start_datetime >= order.end_datetime:
        raise ValidationError(_("The dates is incorrect"))
    try:
        # TODO: test it
        if order.duration % order.service.duration != 0:
            raise ValidationError(
                _("The duration must be a multiple of the service duration"))
        if model.objects.get_overlapping_entries(order).count():
            raise ValidationError(_("Orders should not overlap"))
    except ObjectDoesNotExist as error:
        raise ValidationError(_("The service or client is empty")) from error


def validate_order_status(order: "Order"):
    """Validate the order status."""
    if order.start_datetime <= arrow.utcnow().datetime \
            and order.status == order.STATUS_CANCELED:
        raise ValidationError(_("Orders in the past cannot be canceled"))


# TODO: test it
def validate_order_service_location(order: "Order"):
    """Validate the order service location."""
    try:
        service = order.service
        if not service.service_type == service.TYPE_PROFESSIONAL_LOCATION:
            return
        location = order.service_location
        if not location:
            raise ValidationError(_("The service location is empty"))
        if location.service != service:
            raise ValidationError(
                _("The service location from the other service"))
    except ObjectDoesNotExist as error:
        raise ValidationError(
            _("The service or service location is empty")) from error


# TODO: test it
def validate_order_client_location(order: "Order"):
    """Validate the order client location."""
    try:
        service = order.service
        if not service.service_type == service.TYPE_CLIENT_LOCATION:
            return
        location = order.client_location
        if not location:
            raise ValidationError(_("The client location is empty"))
        if location.user != order.client:
            raise ValidationError(_("The client location from the other user"))
    except ObjectDoesNotExist as error:
        raise ValidationError(
            _("The service, client, or client location is empty")) from error


def validate_order_client(order: "Order"):
    """Validate the order client."""
    try:
        if order.service.professional.user == order.client:
            raise ValidationError(
                "The client and the professional are identical.")
        if not order.first_name or not order.last_name:
            raise ValidationError(_("The name is empty"))
        if not order.phone:
            raise ValidationError(_("The phone is empty"))

    except ObjectDoesNotExist as error:
        raise ValidationError(_("The service or client is empty")) from error


def validate_order_availability(order: "Order"):
    """Validate the order availability."""
    if order.status in [order.STATUS_COMPLETED, order.STATUS_CANCELED]:
        return
    if not order.service.is_enabled:
        raise ValidationError("The service is disabled")

    # new order
    if not order.pk:
        _validate_slots(
            arrow.get(order.start_datetime),
            arrow.get(order.end_datetime),
            order.service,
        )
        return

    manager = apps.get_model("orders", "Order").objects
    saved_order: "Order" = manager.get(pk=order.pk)

    # the edited order does not overlap with the existing order
    if order.end_datetime <= saved_order.start_datetime or \
            order.start_datetime >= saved_order.end_datetime:
        _validate_slots(
            order.start_datetime,
            order.end_datetime,
            order.service,
        )
    # the edited order overlaps with the existing order
    else:
        # tail
        if order.start_datetime < saved_order.start_datetime:
            _validate_slots(
                order.start_datetime,
                saved_order.start_datetime,
                order.service,
            )
        # head
        if order.end_datetime > saved_order.end_datetime:
            _validate_slots(
                saved_order.end_datetime,
                order.end_datetime,
                order.service,
            )


def _validate_slots(
    start: datetime,
    end: datetime,
    service: "Service",
):
    """Validate the availability slots."""
    slots = AvailabilitySlot.objects.get_encompassing_interval(
        arrow.get(start),
        arrow.get(end),
        service,
    )
    if not slots.count():
        raise ValidationError("Availability slots not found")
