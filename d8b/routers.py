"""The d8b router module."""
from rest_framework.routers import DefaultRouter as BaseRouter

from communication.routers import get_router as get_communication_router
from contacts.routers import get_router as get_contacts_router
from location.routers import get_router as get_location_router
from orders.routers import get_router as get_orders_router
from professionals.routers import get_router as get_professionals_router
from schedule.routers import get_router as get_schedule_router
from search.routers import get_router as get_search_router
from services.routers import get_router as get_services_router
from users.routers import get_router as get_users_router


class DefaultRouter(BaseRouter):
    """The default router class."""

    def extend(self, *args):
        """Extend the default router with other routers."""
        for router in args:
            self.registry.extend(router.registry)


def get_router_urls() -> list:
    """Return the default router URLs."""
    router = DefaultRouter()
    router.extend(get_location_router())
    router.extend(get_users_router())
    router.extend(get_contacts_router())
    router.extend(get_professionals_router())
    router.extend(get_communication_router())
    router.extend(get_services_router())
    router.extend(get_schedule_router())
    router.extend(get_orders_router())
    router.extend(get_search_router())
    return router.urls
