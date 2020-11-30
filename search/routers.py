"""The search routers module."""
from rest_framework.routers import SimpleRouter

from .views import SearchViewSet


def get_router() -> SimpleRouter:
    """Return the app router."""
    router = SimpleRouter()
    router.register(
        r"search",
        SearchViewSet,
        "search",
    )
    return router
