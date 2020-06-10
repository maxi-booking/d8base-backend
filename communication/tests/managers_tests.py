"""The services tests module."""
from decimal import Decimal

import pytest
from django.db.models.query import QuerySet

from communication.models import Message, Review
from conftest import OBJECTS_TO_CREATE
from users.models import User

pytestmark = pytest.mark.django_db


def test_review_manager_get_user_list(
    user: User,
    reviews: QuerySet,
):
    """Should return a professional list filtered by a the user."""
    assert reviews.count() == 2
    result = Review.objects.get_user_list(user)
    assert result.count() == 1
    assert result.first().professional.user == user


def test_review_manager_get_professional_rating(
    admin: User,
    professionals: QuerySet,
):
    """Should return the professional rating."""
    manager = Review.objects
    user_manager = User.objects
    professional = professionals.first()
    assert manager.get_professional_rating(professional) is None

    manager.create(
        user=admin,
        professional=professional,
        description='description',
        rating=4,
    )
    assert manager.get_professional_rating(professional) == Decimal(4.00)

    manager.create(
        user=user_manager.create_user('one@example.com', 'pass'),
        professional=professional,
        description='description',
        rating=5,
    )
    assert manager.get_professional_rating(professional) == Decimal(4.50)

    manager.create(
        user=user_manager.create_user('two@example.com', 'pass'),
        professional=professional,
        description='description',
        rating=1,
    )
    assert manager.get_professional_rating(professional) == Decimal(3.33)


def test_get_sent_messages(admin: User, messages: QuerySet):
    """Should return sent messages."""
    manager = Message.objects
    query = manager.get_sent_messages(admin)
    num = OBJECTS_TO_CREATE
    message = query.first()
    message.is_deleted_from_sender = True
    message.save()

    query = manager.get_sent_messages(admin)
    assert num - 1 == query.count()
    assert num != messages.count()

    message = query.first()
    message.is_read = True
    message.save()
    assert num - 2 == manager.get_sent_messages(admin, is_read=False).count()


def test_get_received_messages(admin: User, messages: QuerySet):
    """Should return received messages."""
    manager = Message.objects
    query = manager.get_received_messages(admin)
    num = OBJECTS_TO_CREATE
    message = query.first()
    message.is_deleted_from_recipient = True
    message.save()

    query = manager.get_received_messages(admin)
    assert num - 1 == query.count()
    assert num != messages.count()

    message = query.first()
    message.is_read = True
    message.save()
    assert num - 2 == manager.get_received_messages(admin,
                                                    is_read=False).count()
