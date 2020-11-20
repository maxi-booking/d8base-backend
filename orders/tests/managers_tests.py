"""The managers test module."""

import arrow
import pytest
from django.conf import settings
from django.db.models import QuerySet

from orders.models import Order, OrderReminder
from services.models import Service

pytestmark = pytest.mark.django_db


def test_order_reminder_manager_get_for_notification(
        orders: "QuerySet[Order]"):
    """Should return a list of reminders to notify.."""
    step: int = settings.D8B_REMINDER_INTERVAL
    order: Order = orders.first()
    for i in range(1, 5):
        reminder = OrderReminder()
        reminder.order = order
        reminder.recipient = order.client
        reminder.remind_before = i * step
        reminder.save()

    manager = OrderReminder.objects
    assert not manager.get_for_notification().count()

    order.start_datetime = arrow.utcnow().shift(minutes=-1).datetime
    reminder.order = order
    reminder.remind_before_datetime = step
    reminder.save()

    assert manager.get_for_notification().count() == 1

    reminder.is_reminded = True
    reminder.save()

    assert not manager.get_for_notification().count()


def test_order_manager_get_overlapping_entries(orders: QuerySet):
    """Should return the overlapping entries."""
    manager = Order.objects
    order = orders.last()
    assert not manager.get_overlapping_entries(order).count()

    order.start_datetime = arrow.utcnow().shift(days=1, hours=4).datetime
    order.end_datetime = arrow.utcnow().shift(days=1, hours=14).datetime
    assert manager.get_overlapping_entries(order).count()

    order.start_datetime = arrow.utcnow().shift(days=1, hours=8).datetime
    order.end_datetime = arrow.utcnow().shift(days=1, hours=9).datetime
    assert manager.get_overlapping_entries(order).count()


def test_order_manager_get_between_dates(orders: QuerySet):
    """Should return the entries between dates."""
    now = arrow.utcnow()
    order = orders.last()
    order.service.is_enabled = True
    Service.objects.update(is_enabled=True)
    manager = Order.objects

    assert manager.get_between_dates(
        now,
        now.shift(days=2),
        professional=order.service.professional,
    ).count() == 2

    assert manager.get_between_dates(
        now,
        now.shift(days=2),
        professional=order.service.professional,
        service=order.service,
    ).count() == 1
