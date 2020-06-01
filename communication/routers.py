"""The professionals routers module."""
from push_notifications.api.rest_framework import GCMDeviceAuthorizedViewSet
from rest_framework.routers import SimpleRouter

from .views import (ReceivedMessagesViewSet, SentMessagesViewSet,
                    UserReviewViewSet)


def get_router() -> SimpleRouter:
    """Return the app router."""
    router = SimpleRouter()
    router.register(
        r'accounts/reviews',
        UserReviewViewSet,
        'user-reviews',
    )
    router.register(
        r'communication/devices/fcm',
        GCMDeviceAuthorizedViewSet,
        'communication-devices-fmc',
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
    return router
