"""The services filtersets module."""
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters

from professionals.filtersets import _get_professionals

from .models import Price, Service, ServiceLocation, ServicePhoto, ServiceTag


# TODO: test it
def _get_services(request: HttpRequest) -> QuerySet:
    """Get a list of services."""
    if not request:
        return Service.objects.none()
    return Service.objects.get_user_list(user=request.user)


class ServiceFilterSet(filters.FilterSet):
    """The filter class for the service viewset class."""

    professional = filters.ModelChoiceFilter(
        label=_('professional'),
        queryset=_get_professionals,
    )

    class Meta:
        """The metainformation."""

        model = Service
        fields = ('professional', 'is_enabled', 'is_base_schedule')


class ServicePhotoFilterSet(filters.FilterSet):
    """The filter class for the service photo viewset class."""

    service = filters.ModelChoiceFilter(
        label=_('service'),
        queryset=_get_services,
    )

    class Meta:
        """The metainformation."""

        model = ServicePhoto
        fields = ('service', )


class ServiceLocationFilterSet(filters.FilterSet):
    """The filter class for the service location viewset class."""

    service = filters.ModelChoiceFilter(
        label=_('service'),
        queryset=_get_services,
    )

    class Meta:
        """The metainformation."""

        model = ServiceLocation
        fields = ('service', )


class ServiceTagFilterSet(filters.FilterSet):
    """The filter class for the service tag viewset class."""

    service = filters.ModelChoiceFilter(
        label=_('service'),
        queryset=_get_services,
    )

    class Meta:
        """The metainformation."""

        model = ServiceTag
        fields = ('service', )


class PriceFilterSet(filters.FilterSet):
    """The filter class for the price viewset class."""

    service = filters.ModelChoiceFilter(
        label=_('service'),
        queryset=_get_services,
    )

    class Meta:
        """The metainformation."""

        model = Price
        fields = ('service', 'is_price_fixed')
