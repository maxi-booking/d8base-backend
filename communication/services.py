"""The communication managers module."""
import arrow

from .models import Message


def delete_message_from_sender(message: Message) -> Message:
    """Delete the message from the sender."""
    message.is_deleted_from_sender = True
    message.delete_from_sender_datetime = arrow.utcnow().datetime
    message.save()

    return message


def delete_message_from_recipient(message: Message) -> Message:
    """Delete the message from the recipient."""
    message.is_deleted_from_recipient = True
    message.is_read = True
    message.delete_from_recipient_datetime = arrow.utcnow().datetime
    message.save()

    return message


def mark_message_read(message: Message) -> Message:
    """Mark the message read."""
    message.is_read = True
    message.read_datetime = arrow.utcnow().datetime
    message.save()

    return message
