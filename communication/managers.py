"""The communication managers module."""
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from django.db import models
from django.db.models.query import QuerySet

from users.models import User

if TYPE_CHECKING:
    from professionals.models import Professional


class ReviewCommentManager(models.Manager):
    """The review comment manager."""

    def get_list(self) -> QuerySet:
        """Return a list of review comments."""
        return self.all().select_related(
            'user',
            'review',
            'review__professional',
            'review__professional__user',
            'review__user',
            'created_by',
            'modified_by',
        )


class ReviewManager(models.Manager):
    """The review manager."""

    def get_list(self) -> QuerySet:
        """Return a list of reviews."""
        return self.all().select_related(
            'user',
            'professional',
            'created_by',
            'modified_by',
        )

    def get_professional_rating(
            self, professional: 'Professional') -> Optional[Decimal]:
        """Get the average professional rating."""
        result = self.filter(professional=professional).\
            aggregate(models.Avg('rating'))['rating__avg']
        return Decimal(round(result, 2)) if result else None

    def get_user_list(self, user: User) -> QuerySet:
        """Return a list filtered by the user."""
        return self.get_list().filter(professional__user=user)


class MessagesManager(models.Manager):
    """The messages manager."""

    def get_list(self) -> QuerySet:
        """Return a list of messages."""
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

    def get_latest_distinct_received_messages(
        self,
        user: Optional[User] = None,
    ) -> QuerySet:
        """Return a list of user latest distinct received messages."""
        subquery = models.Subquery(self.all().distinct('sender__pk').values(
            'pk').order_by('sender__pk'))
        query = self.get_received_messages(user).\
            filter(pk__in=subquery).order_by('-created')

        return query
