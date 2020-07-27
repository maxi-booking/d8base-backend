"""The schedule views module."""
from rest_framework import viewsets

from .filtersets import ProfessionalScheduleFilterSet, ServiceScheduleFilterSet
from .models import ProfessionalSchedule, ServiceSchedule
from .serializers import (ProfessionalScheduleSerializer,
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
