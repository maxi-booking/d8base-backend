"""The professionals routers module."""
from rest_framework.routers import SimpleRouter

from .views import ReceivedMessagesViewSet, SentMessagesViewSet


def get_router() -> SimpleRouter:
    """Return the app router."""
    router = SimpleRouter()
    router.register(
        r'messages/sent',
        SentMessagesViewSet,
        'messages-sent',
    )
    router.register(
        r'messages/received',
        ReceivedMessagesViewSet,
        'messages-received',
    )
    return router
