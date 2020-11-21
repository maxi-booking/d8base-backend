"""The orders fixtures module."""

import arrow
import pytest
from django.conf import settings
from django.db.models.query import QuerySet
from djmoney.money import Money

from orders.models import Order, OrderReminder

# pylint: disable=redefined-outer-name


@pytest.fixture
def orders(
    users: QuerySet,
    professionals: QuerySet,
    services: QuerySet,
) -> "QuerySet[Order]":
    """Return a orders queryset."""
    # pylint: disable=unused-argument
    user = users.first()
    for professional in professionals.distinct("user").order_by("user"):
        service = professional.services.first()
        order = Order()
        order.client = user
        order.start_datetime = arrow.utcnow().shift(hours=2).datetime
        order.end_datetime = arrow.utcnow().shift(hours=4).datetime
        order.service = service
        order.note = f"note {service.pk}"
        order.remind_before = 60
        order.price = Money(10, "USD")
        order.save()

        service = professional.services.last()
        order = Order()
        order.client = user
        order.start_datetime = arrow.utcnow().shift(hours=6, days=1).datetime
        order.end_datetime = arrow.utcnow().shift(hours=10, days=1).datetime
        order.service = service
        order.note = f"note {service.pk}"
        order.save()
    return Order.objects.get_list()


@pytest.fixture
def order_reminders(
    user: QuerySet,
    admin: QuerySet,
    orders: QuerySet,
) -> "QuerySet[Order]":
    """Return a order reminders queryset."""
    step: int = settings.D8B_REMINDER_INTERVAL
    for order in orders:
        reminder = OrderReminder()
        reminder.order = order
        reminder.recipient = admin
        reminder.remind_before = step * 2
        reminder.save()

        reminder = OrderReminder()
        reminder.order = order
        reminder.recipient = user
        reminder.remind_before = step
        reminder.is_reminded = True
        reminder.save()
    return OrderReminder.objects.get_list()
