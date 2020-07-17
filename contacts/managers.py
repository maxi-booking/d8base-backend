"""The contacts managers module."""
from typing import Optional

from cities.models import Country
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet


class ContactsManager(models.Manager):
    """The contacts  manager."""

    def get_by_country(
        self,
        country: Country,
        queryset: Optional[QuerySet] = None,
    ) -> QuerySet:
        """Return a list of contacts available for the specified country."""
        if not queryset:
            queryset = self.get_list()
        return queryset.\
            filter(Q(countries=None) | Q(countries=country)).\
            exclude(excluded_countries=country)

    def get_list(self) -> QuerySet:
        """Return a list of contacts."""
        return self.all().\
            select_related("created_by", "modified_by").\
            prefetch_related("countries", "excluded_countries")
