"""The services tests module."""
import pytest
from pytest_mock import MockFixture

from communication.notifications.messenger import Messenger
from communication.notifications.tasks import send_email
from users.models import User

pytestmark = pytest.mark.django_db


def test_messenger_send(user: User, mocker: MockFixture):
    """Should send messages."""
    mocks = []
    for i in range(0, 4):
        mock = mocker.Mock()
        mock.apply_async = mocker.Mock(return_value=i)
        mocks.append(mock)
    messenger = Messenger()
    messenger.messengers = mocks
    messenger.send(
        user=user,
        subject="test subject",
        template="message_notification",
        context={},
    )
    for mock in mocks:
        assert mock.apply_async.call_count == 1


def test_messenger_init():
    """Should send messages."""
    messenger = Messenger()
    assert isinstance(messenger.messengers[0], type(send_email))
