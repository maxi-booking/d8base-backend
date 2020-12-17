"""The schedule views module."""
from typing import Any, Dict

from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.settings import api_settings

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


class ScheduleSetMixin():
    """The schedule set method mixin."""

    set_delete_attr: str

    def _get_params_for_set_delete(self) -> Dict[str, Any]:
        """Get params for the deletion before the set method."""
        ids = {i[self.set_delete_attr]
               for i in self.request.data}  # type: ignore
        return {f"{self.set_delete_attr}__pk__in": ids}

    @action(detail=False, methods=["post"])
    def set(self, request):
        """Set the schedules."""
        if not isinstance(request.data, list):
            raise ValidationError(
                {
                    api_settings.NON_FIELD_ERRORS_KEY:
                        [_("Invalid data. Expected a list.")]
                }, )
        self.serializer_class.Meta.model.objects.delete_for_user(
            user=request.user, **self._get_params_for_set_delete())
        for entry in request.data:
            serializer = self.get_serializer(data=entry)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

        serializer = self.get_serializer(data=request.data, many=True)
        return Response(
            serializer.initial_data,
            status=status.HTTP_201_CREATED,
        )


class ProfessionalScheduleViewSet(viewsets.ModelViewSet, ScheduleSetMixin):
    """The professional schedule viewset."""

    is_owner_filter_enabled = True
    owner_filter_field = "professional__user"
    serializer_class = ProfessionalScheduleSerializer
    queryset = ProfessionalSchedule.objects.get_list()
    filterset_class = ProfessionalScheduleFilterSet
    set_delete_attr = "professional"


class ServiceScheduleViewSet(viewsets.ModelViewSet, ScheduleSetMixin):
    """The service schedule viewset."""

    is_owner_filter_enabled = True
    owner_filter_field = "service__professional__user"
    serializer_class = ServiceScheduleSerializer
    queryset = ServiceSchedule.objects.get_list()
    filterset_class = ServiceScheduleFilterSet
    set_delete_attr = "service"


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
