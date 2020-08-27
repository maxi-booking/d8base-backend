"""The schedule routers module."""
from rest_framework.routers import SimpleRouter

from .views import (ProfessionalCalendarViewSet,
                    ProfessionalClosedPeriodViewSet,
                    ProfessionalScheduleViewSet, ServiceClosedPeriodViewSet,
                    ServiceScheduleViewSet)


def get_router() -> SimpleRouter:
    """Return the app router."""
    router = SimpleRouter()
    router.register(
        r"accounts/service-closed-periods",
        ServiceClosedPeriodViewSet,
        "user-service-closed-periods",
    )
    router.register(
        r"accounts/professional-closed-periods",
        ProfessionalClosedPeriodViewSet,
        "user-professional-closed-periods",
    )
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
    router.register(
        r"schedule/calendar",
        ProfessionalCalendarViewSet,
        "schedule-calendar",
    )
    return router
