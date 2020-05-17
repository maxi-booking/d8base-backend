"""The filtersets tests module."""
import pytest
from django.db.models.query import QuerySet
from django.http import HttpRequest

from communication.serializer_fields import ParentMessageForeignKey
from conftest import OBJECTS_TO_CREATE

pytestmark = pytest.mark.django_db


def test_parent_message_foreign_key(messages: QuerySet):
    """Should return the filtered list of messages by a user."""
    obj = ParentMessageForeignKey()
    request = HttpRequest()
    user = messages[0].sender
    request.user = user
    obj._context = {'request': request}  # pylint: disable=protected-access
    result = obj.get_queryset()

    assert messages.count() == OBJECTS_TO_CREATE * 2
    assert result.count() == OBJECTS_TO_CREATE
    assert result.first().recipient == user
