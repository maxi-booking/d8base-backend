"""The communication fixtures module."""

import pytest
from django.db.models.query import QuerySet

from communication.models import Message
from conftest import OBJECTS_TO_CREATE
from users.models import User

# pylint: disable=redefined-outer-name


@pytest.fixture
def messages(
    admin: User,
    user: User,
) -> QuerySet:
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
