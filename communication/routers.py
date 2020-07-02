"""The professionals routers module."""
from push_notifications.api.rest_framework import GCMDeviceAuthorizedViewSet
from rest_framework.routers import SimpleRouter

from .views import (LatestMessagesViewSet, MessagesListViewSet,
                    ReceivedMessagesViewSet, SentMessagesViewSet,
                    UserReviewCommentViewSet, UserReviewViewSet)


def get_router() -> SimpleRouter:
    """Return the app router."""
    router = SimpleRouter()
    router.register(
        r'accounts/reviews',
        UserReviewViewSet,
        'user-reviews',
    )
    router.register(
        r'accounts/review-comments',
        UserReviewCommentViewSet,
        'user-review-comments',
    )
    router.register(
        r'communication/devices/fcm',
        GCMDeviceAuthorizedViewSet,
        'communication-devices-fmc',
    )
    router.register(
        r'communication/messages/latest',
        LatestMessagesViewSet,
        'messages-latest',
    )
    router.register(
        r'communication/messages/sent',
        SentMessagesViewSet,
        'messages-sent',
    )
    router.register(
        r'communication/messages/received',
        ReceivedMessagesViewSet,
        'messages-received',
    )
    router.register(
        r'communication/messages/list',
        MessagesListViewSet,
        'messages-list',
    )
    return router
