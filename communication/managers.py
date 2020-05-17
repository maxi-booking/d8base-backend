"""The communication managers module."""
from typing import Optional

from django.db import models
from django.db.models.query import QuerySet

from users.models import User


class MessagesManager(models.Manager):
    """The messages manager."""

    def get_list(self) -> QuerySet:
        """Return a list of user contacts."""
        return self.all().select_related(
            'sender',
            'recipient',
            'created_by',
            'modified_by',
        )

    def get_sent_messages(
        self,
        user: Optional[User] = None,
        is_read: Optional[bool] = None,
    ) -> QuerySet:
        """Return a list of user sent messages."""
        query = self.get_list().filter(is_deleted_from_sender=False)
        if user is not None:
            query = query.filter(recipient=user)
        if is_read is not None:
            query = query.filter(is_read=is_read)
        return query

    def get_received_messages(
        self,
        user: Optional[User] = None,
        is_read: Optional[bool] = None,
    ) -> QuerySet:
        """Return a list of user received messages."""
        query = self.get_list().filter(is_deleted_from_recipient=False)
        if user is not None:
            query = query.filter(recipient=user)
        if is_read is not None:
            query = query.filter(is_read=is_read)
        return query
