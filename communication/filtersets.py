"""The communication filtersets module."""

from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters

from users.models import User

from .models import Message, Review, ReviewComment


def _get_reviews(request: HttpRequest) -> QuerySet:
    """Get a list of reviews."""
    if not request:
        return Review.objects.none()
    return Review.objects.get_user_list(user=request.user)


def _get_recipients(request: HttpRequest) -> QuerySet:
    """Get a list of recipients."""
    if not request:
        return User.objects.none()
    return Message.objects.get_recipients(sender=request.user)


def _get_interlocutors(request: HttpRequest) -> QuerySet:
    """Get a list of interlocutors."""
    if not request:
        return User.objects.none()
    return Message.objects.get_interlocutors(interlocutor=request.user)


def _get_senders(request: HttpRequest) -> QuerySet:
    """Get a list of senders."""
    if not request:
        return User.objects.none()
    return Message.objects.get_senders(recipient=request.user)


class ReviewCommentFilterSet(filters.FilterSet):
    """The filterset class for the review comment viewset class."""

    review = filters.ModelChoiceFilter(
        label=_("review"),
        queryset=_get_reviews,
    )

    class Meta:
        """The professional list filterset class serializer META class."""

        model = ReviewComment
        fields = ("review", "created", "modified")


class MessagesListFilterSet(filters.FilterSet):
    """The filterset class for the messages list viewset class."""

    interlocutor = filters.ModelChoiceFilter(
        label=_("interlocutor"),
        queryset=_get_interlocutors,
        method="interlocutor_filter",
    )

    def interlocutor_filter(self, queryset, name, value):
        """Filter by the interlocutor."""
        # pylint: disable=unused-argument, no-self-use
        return Message.objects.get_by_interlocutor(
            queryset=queryset,
            interlocutor=value,
        )

    class Meta:
        """The metainformation."""

        model = Message
        fields = ("is_read", "interlocutor", "sender", "recipient")


class SentMessagesFilterSet(filters.FilterSet):
    """The filterset class for the sent messages viewset class."""

    recipient = filters.ModelChoiceFilter(
        label=_("recipient"),
        queryset=_get_recipients,
    )

    class Meta:
        """The metainformation."""

        model = Message
        fields = ("is_read", "recipient")


class ReciviedMessagesFilterSet(filters.FilterSet):
    """The filterset class for the recivied messages viewset class."""

    sender = filters.ModelChoiceFilter(
        label=_("sender"),
        queryset=_get_senders,
    )

    class Meta:
        """The metainformation."""

        model = Message
        fields = ("is_read", "sender")
