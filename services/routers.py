"""The services routers module."""
from rest_framework.routers import SimpleRouter

from .views import (PriceViewSet, RateViewSet, ServiceListViewSet,
                    ServiceLocationViewSet, ServicePhotoListViewSet,
                    ServicePhotoViewSet, ServiceTagListViewSet,
                    ServiceTagViewSet, ServiceViewSet)


def get_router() -> SimpleRouter:
    """Return the app router."""
    router = SimpleRouter()
    router.register(
        r"accounts/services",
        ServiceViewSet,
        "user-services",
    )
    router.register(
        r"services/tags",
        ServiceTagListViewSet,
        "service-tags",
    )
    router.register(
        r"services/service-photos",
        ServicePhotoListViewSet,
        "service-photos",
    )
    router.register(
        r"services/services",
        ServiceListViewSet,
        "services",
    )
    router.register(
        r"accounts/service-tags",
        ServiceTagViewSet,
        "user-service-tags",
    )
    router.register(
        r"accounts/service-locations",
        ServiceLocationViewSet,
        "user-service-locations",
    )
    router.register(
        r"accounts/service-prices",
        PriceViewSet,
        "user-service-prices",
    )
    router.register(
        r"accounts/service-photos",
        ServicePhotoViewSet,
        "user-service-photos",
    )
    router.register(
        r"rates",
        RateViewSet,
        "rates",
    )
    return router
