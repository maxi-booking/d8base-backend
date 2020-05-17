"""The services tests module."""
import arrow
import pytest
from django.db.models.query import QuerySet

from communication.services import (delete_message_from_recipient,
                                    delete_message_from_sender,
                                    mark_message_read)

pytestmark = pytest.mark.django_db


def test_mark_message_read(messages: QuerySet):
    """Should mark the message read."""
    message = messages[0]
    now = arrow.utcnow().datetime

    assert not message.is_read

    mark_message_read(message)
    delta = message.read_datetime - now

    assert message.is_read
    assert message.read_datetime
    assert delta.total_seconds() < 1


def test_delete_message_from_recipient(messages: QuerySet):
    """Should delete the message from the recipient."""
    message = messages[0]
    now = arrow.utcnow().datetime

    assert not message.is_deleted_from_recipient
    assert not message.is_read

    delete_message_from_recipient(message)
    delta = message.delete_from_recipient_datetime - now

    assert message.is_deleted_from_recipient
    assert message.is_read
    assert message.delete_from_recipient_datetime
    assert delta.total_seconds() < 1


def test_delete_message_from_sender(messages: QuerySet):
    """Should delete the message from the sender."""
    message = messages[0]
    now = arrow.utcnow().datetime

    assert not message.is_deleted_from_sender

    delete_message_from_sender(message)
    delta = message.delete_from_sender_datetime - now

    assert message.is_deleted_from_sender
    assert message.delete_from_sender_datetime
    assert delta.total_seconds() < 1
