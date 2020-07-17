"""The communication validators module."""
from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from .models import Message, Review, ReviewComment


def validate_message_recipient(obj: "Message"):
    """Validate the message recipient."""
    if obj.recipient_id and obj.sender and obj.recipient == obj.sender:
        raise ValidationError(
            {"recipient": _("Sender and recipient is the same user.")})


def validate_message_parent(obj: "Message"):
    """Validate the message parent message."""
    if obj.parent and \
            (not obj.parent.is_read or obj.parent.recipient != obj.sender):
        raise ValidationError({"parent": _("Invalid parent message.")})


def validate_review_user(obj: "Review"):
    """Validate the review user."""
    if obj.user_id and obj.professional and obj.user == obj.professional.user:
        raise ValidationError({
            "user": _("The review user and the professional user are equal.")
        })


def validate_review_comment_user(obj: "ReviewComment"):
    """Validate the review comment user."""
    if obj.user_id and obj.review and obj.user != obj.review.professional.user:
        raise ValidationError({
            "user":
                _("The comment user and the professional user are not equal.")
        })
