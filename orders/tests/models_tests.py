"""The models test module."""

import arrow
import pytest

from orders.models import Order

pytestmark = pytest.mark.django_db


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
    assert order.duration == 12 + 3 * 60

    order.end_datetime = now.shift(minutes=12, hours=3, seconds=45)
    assert order.duration == 12 + 1 + 3 * 60
