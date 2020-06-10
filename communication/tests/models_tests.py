"""The models tests module."""
import pytest
from django.db.models.query import QuerySet
from pytest_mock.plugin import MockFixture

from communication.models import Message, Review, ReviewComment
from d8b.fields import RatingField
from users.models import User

pytestmark = pytest.mark.django_db


def test_message_notifier(user: User, admin: User, mocker: MockFixture):
    """Should run a notifier on save."""
    mock = mocker.patch('communication.models.Message.notifier')
    message = Message()
    message.recipient = user
    message.sender = admin
    message.subject = 'subject'
    message.body = 'body'
    message.save()
    assert mock.call_count == 1


def test_review_notifier(
    user: User,
    professionals: QuerySet,
    mocker: MockFixture,
):
    """Should run a notifier on save."""
    mock = mocker.patch('communication.models.Review.notifier')
    professional = professionals.exclude(user=user).first()
    review = Review()
    review.user = user
    review.professional = professional
    review.title = 'title'
    review.description = 'description'
    review.rating = RatingField.GOOD
    review.save()
    assert mock.call_count == 1


def test_review_comment_notifier(
    user: User,
    reviews: QuerySet,
    mocker: MockFixture,
):
    """Should run a notifier on save."""
    mock = mocker.patch('communication.models.ReviewComment.notifier')
    review = reviews.exclude(professional__user=user).first()
    comment = ReviewComment()
    comment.user = user
    comment.review = review
    comment.title = 'title'
    comment.description = 'description'
    comment.save()
    assert mock.call_count == 1
