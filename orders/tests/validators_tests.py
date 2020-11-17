"""The validators test module."""

import arrow
import pytest
from django.core.exceptions import ValidationError
from django.db.models import QuerySet

from orders.models import Order
from orders.validators import (validate_order_availability,
                               validate_order_client, validate_order_dates,
                               validate_order_status)
from users.models import User

pytestmark = pytest.mark.django_db


def test_validate_order_dates(user: User, services: QuerySet):
    """Should validate orders dates."""
    service = services.exclude(professional__user=user).first()
    now = arrow.utcnow()
    order = Order()
    with pytest.raises(ValidationError) as error:
        validate_order_dates(order)
    assert "is not set" in str(error)

    order.start_datetime = now.shift(hours=-2).datetime
    order.end_datetime = now.shift(hours=-1).datetime
    with pytest.raises(ValidationError) as error:
        validate_order_dates(order)
    assert "in the future" in str(error)

    order.start_datetime = now.shift(hours=1).datetime
    with pytest.raises(ValidationError) as error:
        validate_order_dates(order)
    assert "in the future" in str(error)

    order.end_datetime = now.shift(minutes=1).datetime
    with pytest.raises(ValidationError) as error:
        validate_order_dates(order)
    assert "is incorrect" in str(error)

    order.start_datetime = now.shift(hours=4).datetime
    order.end_datetime = now.shift(hours=5).datetime
    with pytest.raises(ValidationError) as error:
        validate_order_dates(order)
    assert "service or client is empty" in str(error)

    order.service = service
    order.client = user

    with pytest.raises(ValidationError) as error:
        validate_order_dates(order)
    assert "be a multiple" in str(error)

    order.service.duration = 60
    validate_order_dates(order)
    order.save()

    order.pk = None
    with pytest.raises(ValidationError) as error:
        validate_order_dates(order)
    assert "not overlap" in str(error)

    order.start_datetime = now.shift(hours=5).datetime
    order.end_datetime = now.shift(hours=15).datetime
    validate_order_dates(order)
    order.save()

    order.start_datetime = now.shift(hours=6).datetime
    validate_order_dates(order)


def test_validate_order_client(user: User, services: QuerySet):
    """Should validate orders clients."""
    service_user = services.filter(professional__user=user).first()
    service = services.exclude(professional__user=user).first()
    order = Order()
    with pytest.raises(ValidationError) as error:
        validate_order_client(order)
    assert "service or client is empty" in str(error)
    order.service = service_user
    order.client = user

    with pytest.raises(ValidationError) as error:
        validate_order_client(order)
    assert "identical" in str(error)

    order.service = service
    with pytest.raises(ValidationError) as error:
        validate_order_client(order)
    assert "name is empty" in str(error)

    order.first_name = "first name"
    with pytest.raises(ValidationError) as error:
        validate_order_client(order)
    assert "name is empty" in str(error)

    order.last_name = "last name"
    with pytest.raises(ValidationError) as error:
        validate_order_client(order)
    assert "phone is empty" in str(error)

    order.phone = "phone"
    validate_order_client(order)


def test_validate_order_availability(
    user: User,
    availability_slots: QuerySet,
):
    """Should validate orders availability."""
    # pylint: disable=too-many-statements
    service = availability_slots.exclude(service__isnull=True).first().service
    service.is_base_schedule = False
    service.is_enabled = False
    service.save()
    start = arrow.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    order = Order()
    order.client = user
    order.service = service
    order.start_datetime = start.datetime
    order.end_datetime = start.shift(days=1).datetime
    order.status = Order.STATUS_NOT_CONFIRMED

    with pytest.raises(ValidationError) as error:
        validate_order_availability(order)
    assert "service is disabled" in str(error)

    service.is_enabled = True
    service.save()

    with pytest.raises(ValidationError) as error:
        validate_order_availability(order)
    assert "slots not found" in str(error)

    order.status = Order.STATUS_COMPLETED
    validate_order_availability(order)

    order.status = Order.STATUS_CANCELED
    validate_order_availability(order)

    # save a new order
    order.status = Order.STATUS_CONFIRMED
    order.start_datetime = start.shift(hours=11).datetime
    order.end_datetime = start.shift(hours=15).datetime
    validate_order_availability(order)
    order.save()

    # update the order: less than the saved order
    order.start_datetime = start.shift(hours=13).datetime
    order.end_datetime = start.shift(hours=14).datetime
    validate_order_availability(order)
    order.save()

    # update the order: tail
    order.start_datetime = start.shift(hours=12).datetime
    order.end_datetime = start.shift(hours=14).datetime
    validate_order_availability(order)
    order.save()

    # update the order: head
    order.start_datetime = start.shift(hours=12).datetime
    order.end_datetime = start.shift(hours=14, minutes=30).datetime
    validate_order_availability(order)
    order.save()

    # update the order: head and tail
    order.start_datetime = start.shift(hours=11).datetime
    order.end_datetime = start.shift(hours=15).datetime
    validate_order_availability(order)
    order.save()

    # update the order: the other date
    order.start_datetime = start.shift(hours=11, days=2).datetime
    order.end_datetime = start.shift(hours=15, days=2).datetime
    validate_order_availability(order)
    order.save()

    order.start_datetime = start.shift(hours=11, days=1).datetime
    order.end_datetime = start.shift(hours=15, days=1).datetime
    validate_order_availability(order)
    order.save()


def test_validate_order_status():
    """Should validate orders status."""
    order = Order()
    order.start_datetime = arrow.utcnow().shift(hours=-1).datetime
    order.end_datetime = arrow.utcnow().shift(hours=1).datetime
    order.status = Order.STATUS_CANCELED
    with pytest.raises(ValidationError) as error:
        validate_order_status(order)
    assert "cannot be canceled" in str(error)

    order.start_datetime = arrow.utcnow().shift(hours=1).datetime
    order.end_datetime = arrow.utcnow().shift(hours=2).datetime
    validate_order_status(order)
