"""The communication managers module."""
from typing import TYPE_CHECKING

import arrow
from django.utils.translation import gettext_lazy as _

from communication.notifications import Messenger

if TYPE_CHECKING:
    from typing import Type
    from .models import Message, Review, ReviewComment, AbstractReminder


def notify_reminders(model: "Type[AbstractReminder]"):
    """Notify reminders."""
    for reminder in model.objects.get_for_notification():
        Messenger().send(
            user=reminder.recipient,
            subject=_(reminder.subject),
            template=reminder.template,
            context=reminder.get_data(),
        )
        reminder.is_reminded = True
        reminder.save()


def notify_new_review_comment(comment: "ReviewComment") -> None:
    """Notify about a new review comment."""
    if comment.pk:
        return None
    Messenger().send(
        user=comment.review.user,
        subject=_("You have new review comments"),
        template="review_comment_notification",
        context={
            "title": comment.title,
            "description": comment.description,
            "review": str(comment.review),
        },
    )
    return None


def notify_new_review(review: "Review") -> None:
    """Notify about a new review."""
    if review.pk:
        return None
    Messenger().send(
        user=review.professional.user,
        subject=_("You have new reviews"),
        template="review_notification",
        context={
            "title": review.title,
            "description": review.description,
            "rating": review.rating,
            "user": str(review.user),
        },
    )
    return None


def notify_new_message(message: "Message") -> None:
    """Notify about a new message."""
    if message.pk:
        return None
    Messenger().send(
        user=message.recipient,
        subject=_("You have new messages"),
        template="message_notification",
        context={
            "subject": message.subject,
            "body": message.body,
            "sender": str(message.sender),
        },
    )
    return None


def delete_message_from_sender(message: "Message") -> "Message":
    """Delete the message from the sender."""
    message.is_deleted_from_sender = True
    message.delete_from_sender_datetime = arrow.utcnow().datetime
    message.save()

    return message


def delete_message_from_recipient(message: "Message") -> "Message":
    """Delete the message from the recipient."""
    message.is_deleted_from_recipient = True
    message.is_read = True
    message.delete_from_recipient_datetime = arrow.utcnow().datetime
    message.save()

    return message


def mark_message_read(message: "Message") -> "Message":
    """Mark the message read."""
    message.is_read = True
    message.read_datetime = arrow.utcnow().datetime
    message.save()

    return message
