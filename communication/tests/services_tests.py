"""The services tests module."""
from typing import List

import arrow
import pytest
from django.core.mail import EmailMultiAlternatives
from django.db.models.query import QuerySet

from communication.models import Message, Review, ReviewComment
from communication.services import (delete_message_from_recipient,
                                    delete_message_from_sender,
                                    mark_message_read, notify_new_message,
                                    notify_new_review,
                                    notify_new_review_comment)
from users.models import User

pytestmark = pytest.mark.django_db


def test_notify_new_review_comment(
    user: User,
    reviews: QuerySet,
    mailoutbox: List[EmailMultiAlternatives],
):
    """Should notify about a new review comment."""
    mailoutbox.clear()
    review = reviews.exclude(professional__user=user).first()
    comment = ReviewComment()
    comment.user = user
    comment.review = review
    comment.title = 'title'
    comment.description = 'description'

    notify_new_review_comment(comment)
    assert len(mailoutbox) == 1
    assert review.user.email in mailoutbox[0].recipients()

    notify_new_review_comment(comment)
    assert len(mailoutbox) == 2


def test_notify_new_message(
    user: User,
    admin: User,
    mailoutbox: List[EmailMultiAlternatives],
):
    """Should notify about a new message."""
    message = Message()
    message.recipient = user
    message.sender = admin
    message.subject = 'subject'
    message.body = 'body'

    notify_new_message(message)
    assert len(mailoutbox) == 1
    assert user.email in mailoutbox[0].recipients()

    notify_new_message(message)
    assert len(mailoutbox) == 2


def test_notify_new_review(
    user: User,
    professionals: QuerySet,
    mailoutbox: List[EmailMultiAlternatives],
):
    """Should notify about a new review."""
    professional = professionals.exclude(user=user).first()
    review = Review()
    review.user = user
    review.professional = professional
    review.title = 'title'
    review.description = 'description'

    notify_new_review(review)
    assert len(mailoutbox) == 1
    assert professional.user.email in mailoutbox[0].recipients()

    notify_new_review(review)
    assert len(mailoutbox) == 2


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
