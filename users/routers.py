"""The users routers module."""
from rest_framework.routers import SimpleRouter

from .views import UserLanguageViewSet


def get_router() -> SimpleRouter:
    """Return the app router."""
    router = SimpleRouter()
    router.register(r'accounts/languages', UserLanguageViewSet,
                    'user-languages')

    return router
