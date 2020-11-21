"""The models test module."""
import pytest
from pytest_mock import MockFixture

from orders.models import OrderReminder
from orders.tasks import notify_order_reminders

pytestmark = pytest.mark.django_db


def test_notify_order_reminders(mocker: MockFixture):
    """Should run the notify_remenders."""
    notifier = mocker.patch("orders.tasks.notify_reminders")
    notify_order_reminders()
    notifier.assert_called_once_with(OrderReminder)
