"""The services test module."""

import arrow
import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from djmoney.money import Money
from pytest_mock import MockFixture

from orders.calc import AbstractCalculator
from orders.models import Order
from orders.services import OrderAutoFiller, is_sent_order_updatable
from users.models import User

pytestmark = pytest.mark.django_db

# pylint: disable=protected-access


def test_is_sent_order_updatable(orders: QuerySet):
    """Should check if the sent order can be updated."""
    order = orders.first()
    assert is_sent_order_updatable(order)

    order.start_datetime = arrow.utcnow().shift(seconds=-1).datetime
    assert not is_sent_order_updatable(order)


def test_order_auto_filler_set_status(services: QuerySet):
    """Should set the order status."""
    service = services.first()
    service.is_auto_order_confirmation = False
    order = Order()
    order.service = service
    OrderAutoFiller(order)._set_status()

    assert order.status == order.STATUS_NOT_CONFIRMED

    service.is_auto_order_confirmation = True
    OrderAutoFiller(order)._set_status()
    assert order.status == order.STATUS_CONFIRMED

    order.pk = 1
    order.status = order.STATUS_PAID
    OrderAutoFiller(order)._set_status()

    assert order.status == order.STATUS_PAID


def test_order_auto_filler_set_end_datetime(services: QuerySet):
    """Should set the order end."""
    service = services.first()
    service.duration = 60
    now = arrow.utcnow()
    order = Order()
    order.start_datetime = now.datetime
    order.service = service
    OrderAutoFiller(order)._set_end_datetime()

    assert order.end_datetime == now.shift(minutes=60).datetime

    end = now.shift(days=2).datetime
    order.end_datetime = end
    OrderAutoFiller(order)._set_end_datetime()
    assert order.end_datetime == end


def test_order_auto_filler_set_contacts(user: User):
    """Should set the order contacts."""
    user.first_name = "first name"
    user.last_name = "last name"
    user.phone = "phone"
    order = Order()
    order.client = user

    OrderAutoFiller(order)._set_contacts()

    assert order.first_name == user.first_name
    assert order.last_name == user.last_name
    assert order.phone == user.phone

    order.is_another_person = True
    order.first_name = None
    order.last_name = None
    order.phone = None
    OrderAutoFiller(order)._set_contacts()

    assert order.first_name is None
    assert order.last_name is None
    assert order.phone is None

    order.is_another_person = False
    order.first_name = "new first name"
    order.last_name = "new last name"
    order.phone = "new phone"
    OrderAutoFiller(order)._set_contacts()

    assert order.first_name == "new first name"
    assert order.last_name == "new last name"
    assert order.phone == "new phone"


def test_order_auto_filler_set_price(mocker: MockFixture):
    """Should run the calculator."""
    order = Order()
    filler = OrderAutoFiller(order)
    assert isinstance(filler.calc, AbstractCalculator)
    filler.calc.calc = mocker.MagicMock(return_value=1)  # type: ignore

    order.price = Money(1, "EUR")
    filler._set_price()
    filler.calc.calc.assert_not_called()  # type: ignore

    order.price = None
    filler._set_price()
    filler.calc.calc.assert_called_once()  # type: ignore


def test_order_auto_filler_fill(mocker: MockFixture):
    """Should set the order contacts."""
    order = Order()
    filler = OrderAutoFiller(order)
    filler._set_status = mocker.MagicMock(return_value=1)  # type: ignore
    filler._set_contacts = mocker.MagicMock(return_value=2)  # type: ignore
    filler._set_end_datetime = mocker.MagicMock(return_value=3)  # type: ignore
    filler._set_price = mocker.MagicMock(return_value=4)  # type: ignore
    filler.fill()

    filler._set_status.assert_called_once()  # type: ignore
    filler._set_contacts.assert_called_once()  # type: ignore
    filler._set_end_datetime.assert_called_once()  # type: ignore
    filler._set_price.assert_called_once()  # type: ignore


def test_order_auto_filler_fill_exception(mocker: MockFixture):
    """Should raise the exception."""
    order = Order()
    filler = OrderAutoFiller(order)
    filler._set_status = mocker.MagicMock()  # type: ignore
    filler._set_status.side_effect = ObjectDoesNotExist("test")  # type: ignore
    filler._set_end_datetime = mocker.MagicMock(return_value=3)  # type: ignore
    filler.fill()

    filler._set_status.assert_called_once()  # type: ignore
    filler._set_end_datetime.assert_not_called()  # type: ignore
