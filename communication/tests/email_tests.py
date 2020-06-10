"""The emails tests module."""
import pytest
from tests.fixtures.auth import USER_EMAIL

from communication.notifications.email import mail_managers, mail_user
from users.models import User

pytestmark = pytest.mark.django_db


def test_mail_managers(mailoutbox):
    """Should send an email to the system managers."""
    mail_managers(subject='Text message', data={'text': '<p>Test text</p>'})
    assert len(mailoutbox) == 1
    mail = mailoutbox[0]
    assert mail.recipients() == ['admin@example.com', 'manager@example.com']
    assert 'Text message' in mail.subject
    assert '<p>Test text' in mail.alternatives[0][0]


def test_mail_user(
    user: User,
    mailoutbox,
):
    """Should send an email to the user."""
    mail_user(
        user=user,
        subject='Text message',
        template='message_notification',
        data={},
    )
    assert len(mailoutbox) == 1
    mail = mailoutbox[0]
    assert mail.recipients() == [USER_EMAIL]
    assert 'Text message' in mail.subject
