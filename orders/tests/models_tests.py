"""The models test module."""

import arrow
import pytest
from django.db.models import QuerySet
from pytest_mock import MockFixture

from orders.models import Order, OrderReminder
from users.models import User

pytestmark = pytest.mark.django_db


def test_order_reminder_save(orders: "QuerySet[Order]"):
    """Should set the remind_before_datetime field."""
    order: Order = orders.first()
    reminder = OrderReminder()
    reminder.order = order
    reminder.recipient = order.client
    reminder.remind_before = 30
    reminder.save()

    assert reminder.remind_before_datetime == arrow.get(
        order.start_datetime).shift(minutes=-30).datetime
    assert reminder.is_reminded is False


def test_order_reminder_get_data(orders: "QuerySet[Order]"):
    """Should return the order data."""
    order: Order = orders.first()
    reminder = OrderReminder()
    reminder.order = order

    assert reminder.get_data() == {
        "id": order.pk,
        "note": order.note,
        "price": str(order.price),
        "first_name": order.first_name,
        "last_name": order.last_name,
        "phone": str(order.phone),
        "service": order.service.name,
    }


def test_order_duration():
    """Should return duration of an order."""
    now = arrow.utcnow()
    order = Order()
    order.start_datetime = now.datetime
    order.end_datetime = now.shift(minutes=12)

    assert order.duration == 12

    order.end_datetime = now.shift(minutes=12, hours=3)
    assert order.duration == 12 + 3 * 60

    order.end_datetime = now.shift(minutes=12, hours=3, seconds=15)
    assert order.duration == 192.25

    order.end_datetime = now.shift(minutes=12, hours=3, seconds=45)
    assert order.duration == 192.75


def test_order_clean(mocker: MockFixture):
    """Should run the filler."""
    order = Order()
    order.validators = []
    order.filler = mocker.MagicMock()
    order.clean()
    order.filler.assert_called_once()


def test_order_save(user: User, services: QuerySet, mocker: MockFixture):
    """Should run the filler."""
    order = Order()
    order.validators = []
    order.service = services.first()
    order.client = user
    order.start_datetime = arrow.utcnow().shift(hours=2).datetime
    order.end_datetime = arrow.utcnow().shift(hours=4).datetime
    order.filler = mocker.MagicMock()
    order.save()
    order.filler.assert_called_once()
