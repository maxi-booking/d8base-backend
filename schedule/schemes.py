"""The schedule schemes module."""
from drf_yasg import openapi

from schedule.calendar.request import (CalendarPeriod,
                                       HTTPToCalendarRequestConverter)

from .serializers import ProfessionalCalendarSerializer


class ProfessionalCalendarSchema():
    """The professional calendar schema."""

    list_schema = {
        "manual_parameters": [
            openapi.Parameter(
                HTTPToCalendarRequestConverter.PROFESSIONAL_PARAM,
                openapi.IN_QUERY,
                description="professional pk",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                HTTPToCalendarRequestConverter.SERVICE_PARAM,
                openapi.IN_QUERY,
                description="service pk",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                HTTPToCalendarRequestConverter.PERIOD_PARAM,
                openapi.IN_QUERY,
                description=f"type of period: {CalendarPeriod.values()}",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                HTTPToCalendarRequestConverter.START_DATETIME_PARAM,
                openapi.IN_QUERY,
                description="YYYY-MM-DDTHH:mm:ss (2020-08-23T16:19:43)",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                HTTPToCalendarRequestConverter.END_DATETIME_PARAM,
                openapi.IN_QUERY,
                description="YYYY-MM-DDTHH:mm:ss (2020-08-23T16:19:43)",
                type=openapi.TYPE_STRING,
            ),
        ],
        "responses": {
            200: ProfessionalCalendarSerializer(many=True)
        },
    }
