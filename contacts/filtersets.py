"""The contacts filtersets module."""
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters

from location.repositories import CountryRepository

from .models import Contact


class ContactFilterSet(filters.FilterSet):
    """The filter class for the contact viewset class."""

    by_country = filters.ModelChoiceFilter(
        label=_('For country'),
        queryset=CountryRepository().get_list(),
        method='filter_by_country',
    )

    def filter_by_country(self, queryset, _, value):
        """Filter a contact list based on the specified country."""
        # pylint: disable=no-self-use
        return Contact.objects.get_by_country(country=value, queryset=queryset)

    class Meta:
        """The contact filter class serializer META class."""

        model = Contact
        fields = ('by_country', 'countries', 'excluded_countries',
                  'is_default')
