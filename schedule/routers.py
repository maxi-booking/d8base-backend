"""The schedule routers module."""
from rest_framework.routers import SimpleRouter

from .views import ProfessionalScheduleViewSet, ServiceScheduleViewSet


def get_router() -> SimpleRouter:
    """Return the app router."""
    router = SimpleRouter()
    router.register(
        r"accounts/service-schedule",
        ServiceScheduleViewSet,
        "user-service-schedule",
    )
    router.register(
        r"accounts/professional-schedule",
        ProfessionalScheduleViewSet,
        "user-professional-schedule",
    )
    return router
