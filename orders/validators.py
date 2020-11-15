"""The orders validators module."""
from typing import TYPE_CHECKING

import arrow
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.translation import gettext_lazy as _

from d8b.validators import validate_datetime_in_future
from schedule.models import AvailabilitySlot

if TYPE_CHECKING:
    from .models import Order


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
        if model.objects.get_overlapping_entries(order).count():
            raise ValidationError(_("Orders should not overlap"))
    except ObjectDoesNotExist as error:
        raise ValidationError(_("The service or client is empty")) from error


def validate_order_status(order: "Order"):
    """Validate the order status."""
    if order.start_datetime <= arrow.utcnow().datetime \
            and order.status == order.STATUS_CANCELED:
        raise ValidationError(_("Orders in the past cannot be canceled"))


def validate_order_client(order: "Order"):
    """Validate the order client."""
    try:
        if order.service.professional.user == order.client:
            raise ValidationError(
                "The client and the professional are identical.")
    except ObjectDoesNotExist as error:
        raise ValidationError(_("The service or client is empty")) from error


def validate_order_availability(order: "Order"):
    """Validate the order availability."""
    if order.status in [order.STATUS_COMPLETE, order.STATUS_CANCELED]:
        return
    slots = AvailabilitySlot.objects.get_encompassing_interval(
        arrow.get(order.start_datetime),
        arrow.get(order.end_datetime),
        order.service,
    )
    if not slots.count():
        raise ValidationError("Availability slots not found")
