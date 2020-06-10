"""The services tests module."""
import pytest
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet

from communication.models import Review, ReviewComment
from communication.validators import (validate_message_parent,
                                      validate_message_recipient,
                                      validate_review_comment_user,
                                      validate_review_user)
from users.models import User

pytestmark = pytest.mark.django_db


def test_validate_review_comment_user(admin: User, reviews: QuerySet):
    """Should validate the review comment user."""
    comment = ReviewComment()
    comment.user = admin
    comment.review = reviews.exclude(professional__user=admin).first()

    with pytest.raises(ValidationError):
        validate_review_comment_user(comment)


def test_validate_review_user(admin: User, professionals: QuerySet):
    """Should validate the review user."""
    review = Review()
    review.user = admin
    review.professional = professionals.filter(user=admin).first()
    review.rating = 3  # type: ignore
    review.description = 'description'

    with pytest.raises(ValidationError):
        validate_review_user(review)


def test_validate_message_recipient(admin: User, messages: QuerySet):
    """Should mark the message read."""
    message = messages.filter(sender=admin).first()
    validate_message_recipient(message)
    message.recipient = admin
    with pytest.raises(ValidationError):
        validate_message_recipient(message)


def test_validate_parent(admin: User, messages: QuerySet):
    """Should validate the message parent message."""
    messages = messages.filter(sender=admin)
    message = messages[0]
    message.parent = messages[1]
    with pytest.raises(ValidationError):
        validate_message_parent(message)
    message.is_read = True
    with pytest.raises(ValidationError):
        validate_message_parent(message)
    message.parent = messages.filter(recipient=admin).first()
    validate_message_parent(message)
