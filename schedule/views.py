"""The schedule views module."""
from rest_framework import viewsets

from .filtersets import (ProfessionalClosedPeriodFilterSet,
                         ProfessionalScheduleFilterSet,
                         ServiceClosedPeriodFilterSet,
                         ServiceScheduleFilterSet)
from .models import (ProfessionalClosedPeriod, ProfessionalSchedule,
                     ServiceClosedPeriod, ServiceSchedule)
from .serializers import (ProfessionalClosedPeriodSerializer,
                          ProfessionalScheduleSerializer,
                          ServiceClosedPeriodSerializer,
                          ServiceScheduleSerializer)


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
