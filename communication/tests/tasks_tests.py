"""The services tests module."""
import pytest
from tests.fixtures.auth import USER_EMAIL

from communication.notifications.tasks import send_email, send_push
from users.models import User

pytestmark = pytest.mark.django_db


def test_send_email(user: User, mailoutbox):
    """Should send an email to the user."""
    send_email.apply_async(
        kwargs={
            'user_id': user.pk,
            'subject': 'Text message',
            'template': 'message_notification',
            'context': {},
        })
    assert len(mailoutbox) == 1
    mail = mailoutbox[0]
    assert mail.recipients() == [USER_EMAIL]
    assert 'Text message' in mail.subject


def test_send_push(user: User, caplog):
    """Should send a push message to the user."""
    send_push(
        user_id=user.pk,
        subject='Text message',
        template='message_notification',
        context={},
    )
    record = caplog.records[0]
    assert 'An push message has been sent to the user' in record.message
