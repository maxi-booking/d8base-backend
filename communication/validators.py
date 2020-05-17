"""The communication validators module."""
from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from .models import Message


def validate_message_recipient(obj: 'Message'):
    """Validate the message recipient."""
    if obj.recipient_id and obj.sender and obj.recipient == obj.sender:
        raise ValidationError(
            {'recipient': _('Sender and recipient is the same user.')})


def validate_message_parent(obj: 'Message'):
    """Validate the message parent message."""
    if obj.parent and \
            (not obj.parent.is_read or obj.parent.recipient != obj.sender):
        raise ValidationError({'parent': _('Invalid parent message.')})
