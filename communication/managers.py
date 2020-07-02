"""The communication managers module."""
from decimal import Decimal
from operator import attrgetter
from typing import TYPE_CHECKING, List, Optional

from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet

from users.models import User

if TYPE_CHECKING:
    from professionals.models import Professional
    from .models import Message


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


class MessageManager(models.Manager):
    """The messages manager."""

    def get_list(self) -> QuerySet:
        """Return a list of messages."""
        return self.all().select_related(
            'sender',
            'recipient',
            'created_by',
            'modified_by',
        )

    def get_by_interlocutor(
        self,
        *,
        interlocutor: User,
        queryset: Optional[QuerySet] = None,
    ) -> QuerySet:
        """Get the interlocutor queryset."""
        if not queryset:
            queryset = self.get_list()
        return queryset.filter(
            Q(recipient=interlocutor, is_deleted_from_recipient=False)
            | Q(sender=interlocutor, is_deleted_from_sender=False))

    def get_recipients(self, *, sender: User) -> QuerySet:
        """Get the recipients queryset."""
        recipient_ids_query = self.get_sent_messages(sender=sender).\
            distinct('recipient__pk').\
            values('recipient__pk').\
            order_by('recipient__pk')
        return User.objects.filter(
            pk__in=models.Subquery(recipient_ids_query)).distinct('pk')

    def get_senders(self, *, recipient: User) -> QuerySet:
        """Get the senders queryset."""
        sender_ids_query = self.get_received_messages(recipient=recipient).\
            distinct('sender__pk').\
            values('sender__pk').\
            order_by('sender__pk')
        return User.objects.filter(
            pk__in=models.Subquery(sender_ids_query)).distinct('pk')

    def get_interlocutors(self, *, interlocutor: User) -> QuerySet:
        """Get a list of interlocutors of the user."""
        recipients = self.get_recipients(sender=interlocutor).values('pk')
        senders = self.get_senders(recipient=interlocutor).values('pk')
        return User.objects.filter(
            Q(pk__in=models.Subquery(recipients))
            | Q(pk__in=models.Subquery(senders))).distinct('pk')

    def get_sent_messages(
        self,
        sender: Optional[User] = None,
        is_read: Optional[bool] = None,
    ) -> QuerySet:
        """Return a list of user sent messages."""
        query = self.get_list().filter(is_deleted_from_sender=False)
        if sender is not None:
            query = query.filter(sender=sender)
        if is_read is not None:
            query = query.filter(is_read=is_read)
        return query

    def get_received_messages(
        self,
        recipient: Optional[User] = None,
        is_read: Optional[bool] = None,
    ) -> QuerySet:
        """Return a list of user received messages."""
        query = self.get_list().filter(is_deleted_from_recipient=False)
        if recipient is not None:
            query = query.filter(recipient=recipient)
        if is_read is not None:
            query = query.filter(is_read=is_read)
        return query

    def mark_read(
        self,
        *,
        recipient: User,
        sender: User,
        query: Optional[QuerySet] = None,
    ):
        """Mark messages as read."""
        if not query:
            query = self.all()
        query.filter(
            recipient=recipient,
            sender=sender,
        ).update(is_read=True)

    def get_latest_distinct_messages(
        self,
        interlocutor: User,
    ) -> List['Message']:
        """Return a list of user latest distinct messages."""
        received = self.get_received_messages(
            recipient=interlocutor).distinct('sender').order_by(
                'sender',
                '-created',
            )
        sent = self.get_sent_messages(
            sender=interlocutor).distinct('recipient').order_by(
                'recipient',
                '-created',
            )
        latest = {}

        for message in received:
            latest[message.sender] = message

        for message in sent:
            if message.recipient not in latest:
                latest[message.recipient] = message
                continue
            if message.created > latest[message.recipient].created:
                latest[message.recipient] = message

        result = list(latest.values())
        result.sort(key=attrgetter('created'), reverse=True)
        return result
