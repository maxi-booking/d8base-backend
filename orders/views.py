"""The orders views module."""
from typing import Optional

from django.utils.translation import gettext_lazy as _
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from .models import Order
from .serializers import ReceivedOrderSerializer, SentOrderSerializer
from .services import is_sent_order_updatable


class ReceivedOrdersViewSet(
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet,
):
    """The received messages viewset."""

    is_owner_filter_enabled = True
    owner_filter_field = "service__professional__user"
    serializer_class = ReceivedOrderSerializer
    queryset = Order.objects.get_list()

    search_fields = ("=id", "note", "first_name", "last_name", "phone",
                     "client__first_name", "client__last_name",
                     "client__email", "service__name", "service__description")

    filterset_fields = {
        "start_datetime": ["gte", "lte", "exact", "gt", "lt"],
        "end_datetime": ["gte", "lte", "exact", "gt", "lt"],
        "is_another_person": ["exact"],
        "status": ["in"],
    }


class SentOrdersViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet,
):
    """The sent messages viewset."""

    is_owner_filter_enabled = True
    owner_filter_field = "client"
    serializer_class = SentOrderSerializer
    queryset = Order.objects.get_list()
    search_fields = ("=id", "note", "first_name", "last_name", "phone",
                     "service__name", "service__description",
                     "service__professional__name",
                     "=service__professional__id",
                     "service__professional__description",
                     "service__professional__user__first_name",
                     "service__professional__user__last_name")

    filterset_fields = {
        "start_datetime": ["gte", "lte", "exact", "gt", "lt"],
        "end_datetime": ["gte", "lte", "exact", "gt", "lt"],
        "is_another_person": ["exact"],
        "status": ["in"],
    }

    def _check_update_permission(self) -> Optional[Response]:
        if not is_sent_order_updatable(self.get_object()):
            return Response(
                {"error": _("Updating a started order is forbiden.")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return None

    def perform_update(self, serializer):
        """Save the object."""
        serializer.save(price=None)

    def update(self, request, *args, **kwargs):
        """Update the object."""
        # pylint: disable=no-member
        print(request.data)
        return self._check_update_permission() or \
            super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Partial update the object."""
        # pylint: disable=no-member
        print(request.data)
        return self._check_update_permission() or \
            super().partial_update(request, *args, **kwargs)
