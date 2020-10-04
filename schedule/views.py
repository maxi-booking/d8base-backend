"""The schedule views module."""
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from d8b.viewsets import AllowAnyViewSetMixin
from schedule.calendar.exceptions import CalendarError
from schedule.calendar.generator import get_calendar_generator
from schedule.calendar.request import HTTPToCalendarRequestConverter

from .filtersets import (ProfessionalClosedPeriodFilterSet,
                         ProfessionalScheduleFilterSet,
                         ServiceClosedPeriodFilterSet,
                         ServiceScheduleFilterSet)
from .models import (ProfessionalClosedPeriod, ProfessionalSchedule,
                     ServiceClosedPeriod, ServiceSchedule)
from .schemes import ProfessionalCalendarSchema
from .serializers import (ProfessionalCalendarSerializer,
                          ProfessionalClosedPeriodSerializer,
                          ProfessionalScheduleSerializer,
                          ServiceClosedPeriodSerializer,
                          ServiceScheduleSerializer)


class ProfessionalCalendarViewSet(AllowAnyViewSetMixin, viewsets.ViewSet):
    """The professional calendar viewset."""

    serializer_class = ProfessionalCalendarSerializer

    @swagger_auto_schema(**ProfessionalCalendarSchema.list_schema)
    def list(self, request: Request):
        """Return the professional calendar."""
        try:
            converter = HTTPToCalendarRequestConverter(request)
            calendar_request = converter.get()
            generator = get_calendar_generator()
            response = generator.get(calendar_request)
            serializer = self.serializer_class(instance=response, many=True)
        except CalendarError as error:
            raise ValidationError({"error": str(error)}) from error

        return Response(serializer.data)


class ProfessionalScheduleViewSet(viewsets.ModelViewSet):
    """The professional schedule viewset."""

    is_owner_filter_enabled = True
    owner_filter_field = "professional__user"
    serializer_class = ProfessionalScheduleSerializer
    queryset = ProfessionalSchedule.objects.get_list()
    filterset_class = ProfessionalScheduleFilterSet


class ServiceScheduleViewSet(viewsets.ModelViewSet):
    """The service schedule viewset."""

    is_owner_filter_enabled = True
    owner_filter_field = "service__professional__user"
    serializer_class = ServiceScheduleSerializer
    queryset = ServiceSchedule.objects.get_list()
    filterset_class = ServiceScheduleFilterSet


class ProfessionalClosedPeriodViewSet(viewsets.ModelViewSet):
    """The professional closed period viewset."""

    is_owner_filter_enabled = True
    owner_filter_field = "professional__user"
    serializer_class = ProfessionalClosedPeriodSerializer
    queryset = ProfessionalClosedPeriod.objects.get_list()
    filterset_class = ProfessionalClosedPeriodFilterSet


class ServiceClosedPeriodViewSet(viewsets.ModelViewSet):
    """The service closed period viewset."""

    is_owner_filter_enabled = True
    owner_filter_field = "service__professional__user"
    serializer_class = ServiceClosedPeriodSerializer
    queryset = ServiceClosedPeriod.objects.get_list()
    filterset_class = ServiceClosedPeriodFilterSet
