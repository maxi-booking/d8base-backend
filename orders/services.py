"""The orders services module."""
from datetime import timedelta
from typing import TYPE_CHECKING, List

import arrow
from django.core.exceptions import ObjectDoesNotExist
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from communication.notifications import Messenger
from d8b.settings import get_settings

from .calc import AbstractCalculator

if TYPE_CHECKING:
    from users.models import User
    from .models import Order


def notify_order_update(order: "Order", is_created: bool = False) -> None:
    """Notify the users about the order update."""
    professional_user = order.service.professional.user
    client = order.client
    if is_created:
        subject = _("A new order has been created")
    else:
        subject = _("Order has been updated")
    subject += f" #{order.pk}"

    users: List["User"] = []

    updater = order.modified_by if order.modified_by else order.created_by

    if professional_user != updater:
        users.append(professional_user)
    if client != updater:
        users.append(client)

    for user in users:
        Messenger().send(
            user=user,
            subject=subject,
            template="order_update_notification",
            context={
                "id": order.pk,
                "is_created": is_created,
                "note": order.note,
                "price": str(order.price),
                "first_name": order.first_name,
                "last_name": order.last_name,
                "phone": str(order.phone),
                "service": order.service.name,
            },
        )


def copy_contacts_from_order_to_user(order: "Order") -> None:
    """Copy the contacts from the order to its client."""
    if order.is_another_person:
        return
    user: "User" = order.client
    changed = False
    for field in ("first_name", "last_name", "phone"):
        value = getattr(order, field, None)
        if not getattr(user, field, None) and value:
            setattr(user, field, value)
            changed = True
    if changed:
        user.save()


def is_sent_order_updatable(order: "Order") -> bool:
    """Check if the order can be updated."""
    return order.start_datetime > arrow.utcnow().datetime


class OrderAutoFiller():
    """The order filler."""

    order: "Order"
    calc: AbstractCalculator

    def __init__(self, order: "Order") -> None:
        """Construct the object."""
        self.order = order
        self.calc = import_string(get_settings("D8B_CALC"))()

    def _set_status(self):
        """Set the status of the order."""
        if self.order.pk:
            return
        if self.order.service.is_auto_order_confirmation:
            self.order.status = self.order.STATUS_CONFIRMED

    def _set_end_datetime(self):
        """Set the status of the order."""
        if self.order.end_datetime:
            return
        self.order.end_datetime = self.order.start_datetime + timedelta(
            minutes=self.order.service.duration)

    def _set_contacts(self):
        """Set the user contacts."""
        if self.order.is_another_person:
            return
        if not self.order.first_name:
            self.order.first_name = self.order.client.first_name
        if not self.order.last_name:
            self.order.last_name = self.order.client.last_name
        if not self.order.phone:
            self.order.phone = self.order.client.phone

    def _set_price(self):
        """Set the price."""
        if self.order.price:
            return
        self.order.price = self.calc.calc(self.order)

    def fill(self):
        """Fill the order."""
        try:
            self._set_status()
            self._set_end_datetime()
            self._set_contacts()
            self._set_price()
        except ObjectDoesNotExist:
            pass
