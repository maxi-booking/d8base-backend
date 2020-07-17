"""The services tests module."""
from decimal import Decimal
from typing import List

import pytest
from django.db.models import Q
from django.db.models.query import QuerySet

from communication.models import Message, Review
from conftest import OBJECTS_TO_CREATE, USER_EMAIL
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
        description="description",
        rating=4,
    )
    assert manager.get_professional_rating(professional) == Decimal(4.00)

    manager.create(
        user=user_manager.create_user("one@example.com", "pass"),
        professional=professional,
        description="description",
        rating=5,
    )
    assert manager.get_professional_rating(professional) == Decimal(4.50)

    manager.create(
        user=user_manager.create_user("two@example.com", "pass"),
        professional=professional,
        description="description",
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
    message = query.first()
    assert num - 1 == query.count()
    assert num != messages.count()
    assert message.sender == admin

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
    message = query.first()
    assert num - 1 == query.count()
    assert num != messages.count()
    assert message.recipient == admin

    message.is_read = True
    message.save()
    assert num - 2 == manager.get_received_messages(
        admin,
        is_read=False,
    ).count()


def test_message_manager_mark_read(
    admin: User,
    user: User,
    messages: QuerySet,
):
    """Should mark messages as read."""
    assert messages.filter(
        recipient=admin,
        sender=user,
        is_read=False,
    ).count() > 0
    Message.objects.mark_read(recipient=admin, sender=user)
    assert messages.filter(
        recipient=admin,
        sender=user,
        is_read=False,
    ).count() == 0


def test_message_manager_get_by_interlocutor(
    admin: User,
    messages: QuerySet,
):
    """Should return messages filtered by an interlocutor."""
    # pylint: disable=unused-argument
    result = Message.objects.get_by_interlocutor(interlocutor=admin)
    assert result.count() == OBJECTS_TO_CREATE * 2


def test_message_manager_get_recipients(
    admin: User,
    messages: QuerySet,
):
    """Should return recipients."""
    # pylint: disable=unused-argument
    result = Message.objects.get_recipients(sender=admin)
    assert result.count() == 1
    assert result.first().email == USER_EMAIL


def test_message_manager_get_senders(
    admin: User,
    messages: QuerySet,
):
    """Should return senders."""
    # pylint: disable=unused-argument
    result = Message.objects.get_senders(recipient=admin)
    assert result.count() == 1
    assert result.first().email == USER_EMAIL


def test_message_manager_get_interlocutors(
    admin: User,
    users: QuerySet,
    messages: QuerySet,
):
    """Should return interlocutors."""
    # pylint: disable=unused-argument
    user_another = users.first()
    Message.objects.create(
        sender=user_another,
        recipient=admin,
        body="another->admin",
    )
    result = Message.objects.get_interlocutors(interlocutor=admin)
    assert result.count() == 2
    assert result[0].email == user_another.email
    assert result[1].email == USER_EMAIL


def test_message_manager_get_latest_distinct_messages(
    admin: User,
    user: User,
    users: QuerySet,
    messages: QuerySet,
):
    """Should return a list of user latest distinct messages."""
    user_another = users.first()

    def request() -> List[Message]:
        """Make request."""
        return Message.objects.get_latest_distinct_messages(admin)

    obj = messages.filter(Q(recipient=admin) | Q(sender=admin)).\
        order_by("-created").first()
    data = request()
    assert len(data) == 1
    assert data[0] == obj

    Message.objects.create(
        sender=admin,
        recipient=user,
        body="admin->user",
    )

    data = request()
    assert len(data) == 1
    assert data[0].body == "admin->user"
    assert data[0].sender.email == admin.email

    # Send message to the user from the another user
    Message.objects.create(
        sender=user_another,
        recipient=admin,
        body="another->user",
    )
    data = request()
    assert len(data) == 2
    assert data[0].body == "another->user"
    assert data[0].sender.email == user_another.email
    assert data[0].recipient.email == admin.email

    # Delete message to the user from the another user
    Message.objects.filter(
        sender=user_another,
        recipient=admin,
    ).update(is_deleted_from_recipient=True)
    data = request()
    assert len(data) == 1
