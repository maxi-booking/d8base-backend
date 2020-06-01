"""The communication fixtures module."""

import pytest
from django.db.models.query import QuerySet

from communication.models import Message, Review
from conftest import OBJECTS_TO_CREATE
from users.models import User

# pylint: disable=redefined-outer-name


@pytest.fixture
def messages(admin: User, user: User) -> QuerySet:
    """Return a messages queryset."""
    for i in range(0, OBJECTS_TO_CREATE):
        Message.objects.create(
            sender=admin,
            recipient=user,
            subject=f'subject {i}',
            body=f'message body {i}',
        )
    for i in range(0, OBJECTS_TO_CREATE):
        Message.objects.create(
            sender=user,
            recipient=admin,
            subject=f'subject {i}',
            body=f'message body {i}',
        )
    return Message.objects.get_list()


@pytest.fixture
def reviews(admin: User, user: User, professionals: QuerySet) -> QuerySet:
    """Return a reviews queryset."""
    admin_professional = professionals.filter(user=admin).first()
    user_professional = professionals.filter(user=user).first()
    Review.objects.create(
        user=user,
        professional=admin_professional,
        title='title user',
        description='description user',
        rating=4,
    )
    Review.objects.create(
        user=admin,
        professional=user_professional,
        title='title admin',
        description='description admin',
        rating=5,
    )
    return Review.objects.get_list()
