"""The communication views module."""
from typing import Optional

from rest_framework import status, viewsets
from rest_framework.mixins import (DestroyModelMixin, ListModelMixin,
                                   RetrieveModelMixin)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .filtersets import ReviewCommentFilterSet
from .models import Message, Review, ReviewComment
from .serializers import (LatestReceivedMessageSerializer,
                          ReceivedMessageSerializer, ReviewCommentSerializer,
                          ReviewSerializer, SentMessageSerializer)
from .services import (delete_message_from_recipient,
                       delete_message_from_sender, mark_message_read)


class UserReviewCommentViewSet(viewsets.ModelViewSet):
    """The user review comment viewset."""

    is_owner_filter_enabled = True
    serializer_class = ReviewCommentSerializer
    queryset = ReviewComment.objects.get_list()
    filterset_class = ReviewCommentFilterSet
    search_fields = ('=id', 'review__title', 'review__description', 'title',
                     'description', 'review__user__last_name')


class UserReviewViewSet(viewsets.ModelViewSet):
    """The user review viewset."""

    is_owner_filter_enabled = True
    serializer_class = ReviewSerializer
    queryset = Review.objects.get_list()
    filterset_fields = ('rating', 'created', 'modified')
    search_fields = ('=id', 'professional__name', 'professional__description',
                     'title', 'description')


class LatestReceivedMessagesViewSet(viewsets.ReadOnlyModelViewSet):
    """The latest received messages list viewset."""

    is_owner_filter_enabled = True
    owner_filter_field = 'recipient'
    serializer_class = LatestReceivedMessageSerializer
    queryset = Message.objects.get_latest_distinct_received_messages()
    search_fields = ('=id', 'subject', 'body', 'sender__email',
                     'sender__last_name')


class ReceivedMessagesViewSet(RetrieveModelMixin, ListModelMixin,
                              DestroyModelMixin, GenericViewSet):
    """The received messages viewset."""

    is_owner_filter_enabled = True
    owner_filter_field = 'recipient'
    serializer_class = ReceivedMessageSerializer
    queryset = Message.objects.get_received_messages()
    search_fields = ('=id', 'subject', 'sender__last_name', 'sender__email')
    filterset_fields = ('is_read', )
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
    owner_filter_field = 'sender'
    serializer_class = SentMessageSerializer
    queryset = Message.objects.get_sent_messages()
    search_fields = ('=id', 'subject', 'recipient__last_name',
                     'recipient__email')
    filterset_fields = ('is_read', )
    delete_service = delete_message_from_sender

    def _check_update_permission(self) -> Optional[Response]:
        if self.get_object().is_read:
            return Response(
                {'error': 'Updating a read message is forbiden.'},
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
