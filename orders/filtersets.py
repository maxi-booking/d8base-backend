"""The orders filtersets module."""
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters

from services.filtersets import _get_services

from .models import Order


class ReceivedOrdersFilterSet(filters.FilterSet):
    """The filter class for the received order viewset class."""

    service = filters.ModelChoiceFilter(
        label=_("service"),
        queryset=_get_services,
    )

    class Meta:
        """The metainformation."""

        model = Order
        fields = {
            "start_datetime": ["gte", "lte", "exact", "gt", "lt"],
            "end_datetime": ["gte", "lte", "exact", "gt", "lt"],
            "is_another_person": ["exact"],
            "status": ["in"],
        }
