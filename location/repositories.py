"""The location repositories module."""

from abc import ABC, abstractmethod

from cities.models import (AlternativeName, City, Continent, Country, District,
                           Place, PostalCode, Region, Subregion)
from django.db.models.query import QuerySet


class BaseRepository(ABC):
    """The base repository."""

    @property
    @abstractmethod
    def model(self):
        """Return the repository model."""

    @abstractmethod
    def get_list(self):
        """Return a list of objects."""

    def get_or_create(self, **kwargs) -> Place:
        """Get or create an object."""
        return self.model.objects.get_or_create(**kwargs)[0]

    def get_all(self) -> QuerySet:
        """Return all objects."""
        return self.model.objects.all()


class ContinentRepository(BaseRepository):
    """The Continent manager."""

    model = Continent

    def get_list(self) -> QuerySet:
        """Return a list of continents."""
        return self.get_all().order_by('name').\
            prefetch_related('alt_names')


class CountryRepository(BaseRepository):
    """The Country manager."""

    model = Country

    def get_list(self) -> QuerySet:
        """Return a list of countries."""
        return self.get_all().select_related('continent').\
            order_by('name').\
            prefetch_related('neighbours', 'alt_names')


class RegionRepository(BaseRepository):
    """The Region manager."""

    model = Region

    def get_list(self) -> QuerySet:
        """Return a list of regions."""
        return self.get_all().select_related('country').\
            order_by('name').\
            prefetch_related('alt_names')


class SubregionRepository(BaseRepository):
    """The Subregion manager."""

    model = Subregion

    def get_list(self) -> QuerySet:
        """Return a list of subregions."""
        return self.get_all().select_related('region').\
            order_by('name').\
            prefetch_related('alt_names')


class CityRepository(BaseRepository):
    """The City manager."""

    model = City

    def get_list(self) -> QuerySet:
        """Return a list of cities."""
        return self.get_all().\
            select_related('region', 'country', 'subregion').\
            order_by('name').\
            prefetch_related('alt_names')


class DistrictRepository(BaseRepository):
    """The District manager."""

    model = District

    def get_list(self) -> QuerySet:
        """Return a list of districts."""
        return self.get_all().order_by('name').\
            select_related('city').prefetch_related('alt_names')


class PostalCodeRepository(BaseRepository):
    """The PostalCode manager."""

    model = PostalCode

    def get_list(self) -> QuerySet:
        """Return a list of postal codes."""
        return self.get_all().order_by('id').select_related(
            'country',
            'region',
            'subregion',
            'city',
            'district',
        ).prefetch_related('alt_names')


class AlternativeNameRepository(BaseRepository):
    """The AlternativeName manager."""

    model = AlternativeName

    def get_list(self) -> QuerySet:
        """Return a list of alternative names."""
        return self.get_all().order_by('name')
