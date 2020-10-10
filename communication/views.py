"""The communication views module."""
from typing import Optional

from rest_framework import status, viewsets
from rest_framework.mixins import (DestroyModelMixin, ListModelMixin,
                                   RetrieveModelMixin)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .filtersets import (MessagesListFilterSet, ReciviedMessagesFilterSet,
                         ReviewCommentFilterSet, SentMessagesFilterSet)
from .models import Message, Review, ReviewComment, SuggestedMessage
from .serializers import (LatestMessageSerializer, MessageSerializer,
                          ReceivedMessageSerializer, ReviewCommentSerializer,
                          ReviewListSerializer, ReviewSerializer,
                          SentMessageSerializer, SuggestedMessageSerializer)
from .services import (delete_message_from_recipient,
                       delete_message_from_sender, mark_message_read)


class SuggestedMessageViewSet(viewsets.ReadOnlyModelViewSet):
    """The suggested answer viewset."""

    serializer_class = SuggestedMessageSerializer
    queryset = SuggestedMessage.objects.get_list()
    filterset_fields = ("subcategory", "is_enabled")
    search_fields = ("=id", "name", "body")


class UserReviewCommentViewSet(viewsets.ModelViewSet):
    """The user review comment viewset."""

    is_owner_filter_enabled = True
    serializer_class = ReviewCommentSerializer
    queryset = ReviewComment.objects.get_list()
    filterset_class = ReviewCommentFilterSet
    search_fields = ("=id", "review__title", "review__description", "title",
                     "description", "review__user__last_name")


class ReviewListViewSet(viewsets.ReadOnlyModelViewSet):
    """The review list viewset."""

    serializer_class = ReviewListSerializer
    queryset = Review.objects.get_list_with_comments()
    # filterset_fields = ("rating", "professional", "created", "modified")
    search_fields = ("=id", "professional__name", "professional__description",
                     "title", "description")


class UserReviewViewSet(viewsets.ModelViewSet):
    """The user review viewset."""

    is_owner_filter_enabled = True
    serializer_class = ReviewSerializer
    queryset = Review.objects.get_list()
    filterset_fields = ("rating", "professional", "created", "modified")
    search_fields = ("=id", "professional__name", "professional__description",
                     "title", "description")


class LatestMessagesViewSet(viewsets.ViewSet):
    """The latest messages list viewset."""

    permission_classes = [IsAuthenticated]
    serializer_class = LatestMessageSerializer

    def list(self, request):
        """Get a list."""
        queryset = Message.objects.get_latest_distinct_messages(
            interlocutor=request.user)
        serializer = self.serializer_class(list(queryset), many=True)
        return Response(serializer.data)


class MessagesListViewSet(viewsets.ReadOnlyModelViewSet):
    """The readonly messages viewset."""

    serializer_class = MessageSerializer
    queryset = Message.objects.get_list()
    search_fields = ("=id", "subject", "body", "sender__last_name",
                     "sender__email", "recipient__email",
                     "recipient__last_name")

    filterset_class = MessagesListFilterSet

    def mark_read(self, query):
        """Mark messages as read."""
        sender = self.request.GET.get("interlocutor")
        if sender:
            Message.objects.mark_read(
                recipient=self.request.user,
                sender=sender,
                query=query,
            )

    def get_queryset(self):
        """Return the queryset."""
        query = Message.objects.get_by_interlocutor(
            interlocutor=self.request.user,
            queryset=super().get_queryset(),
        )
        self.mark_read(query)
        return query


class ReceivedMessagesViewSet(RetrieveModelMixin, ListModelMixin,
                              DestroyModelMixin, GenericViewSet):
    """The received messages viewset."""

    is_owner_filter_enabled = True
    owner_filter_field = "recipient"
    serializer_class = ReceivedMessageSerializer
    queryset = Message.objects.get_received_messages()
    search_fields = ("=id", "subject", "body", "sender__last_name",
                     "sender__email")
    filterset_fields = ("is_read", )
    filterset_class = ReciviedMessagesFilterSet
    delete_service = delete_message_from_recipient
    read_service = mark_message_read

    def retrieve(self, request, *args, **kwargs):
        """Get the object."""
        # pylint: disable=no-member
        message = self.get_object()
        ReceivedMessagesViewSet.read_service(message)
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Delete the object."""
        message = self.get_object()
        ReceivedMessagesViewSet.delete_service(message)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SentMessagesViewSet(viewsets.ModelViewSet):
    """The sent messages viewset."""

    is_owner_filter_enabled = True
    owner_filter_field = "sender"
    serializer_class = SentMessageSerializer
    queryset = Message.objects.get_sent_messages()
    search_fields = ("=id", "subject", "body", "recipient__last_name",
                     "recipient__email")
    filterset_class = SentMessagesFilterSet
    delete_service = delete_message_from_sender

    def _check_update_permission(self) -> Optional[Response]:
        if self.get_object().is_read:
            return Response(
                {"error": "Updating a read message is forbiden."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return None

    # pylint: disable=no-member
    def update(self, request, *args, **kwargs):
        """Update the object."""
        return self._check_update_permission() or \
            super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Partial update the object."""
        return self._check_update_permission() or \
            super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Delete the object."""
        message = self.get_object()
        if message.is_read:
            SentMessagesViewSet.delete_service(message)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().destroy(self, request, *args, **kwargs)
