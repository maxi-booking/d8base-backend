"""The contacts routers module."""
from rest_framework.routers import SimpleRouter

from .views import ContactViewSet


def get_router() -> SimpleRouter:
    """Return the app router."""
    router = SimpleRouter()
    router.register(r"contacts/contacts", ContactViewSet, "contacts")

    return router
