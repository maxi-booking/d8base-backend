"""The location repositories module."""

from abc import ABC, abstractmethod
from typing import List, Type

from cities.models import (AlternativeName, City, Continent, Country, District,
                           Place, PostalCode, Region, Subregion)
from django.db.models.query import QuerySet


class BaseRepository(ABC):
    """The base repository."""

    @property
    @abstractmethod
    def model(self) -> Type:
        """Return the repository model."""

    @property
    @abstractmethod
    def order_by(self) -> str:
        """Return the default order by."""

    @property
    @abstractmethod
    def select_related(self) -> List[str]:
        """Return the default select_related."""

    @property
    @abstractmethod
    def prefetch_related(self) -> List[str]:
        """Return the default prefetch_related."""

    def get_or_create(self, **kwargs) -> Place:
        """Get or create an object."""
        return self.model.objects.get_or_create(**kwargs)[0]

    def get_all(self) -> QuerySet:
        """Return all objects."""
        return self.model.objects.all()

    def get_list(self) -> QuerySet:
        """Return a list of objects."""
        return self.get_all().order_by(self.order_by).\
            select_related(*self.select_related).\
            prefetch_related(*self.prefetch_related)


class ContinentRepository(BaseRepository):
    """The Continent manager."""

    model = Continent
    order_by: str = 'name'
    select_related: List[str] = []
    prefetch_related: List[str] = ['alt_names']


class CountryRepository(BaseRepository):
    """The Country manager."""

    model = Country
    order_by: str = 'name'
    select_related: List[str] = ['continent']
    prefetch_related: List[str] = ['neighbours', 'alt_names']


class RegionRepository(BaseRepository):
    """The Region manager."""

    model = Region
    order_by: str = 'name'
    select_related: List[str] = ['country']
    prefetch_related: List[str] = ['alt_names']


class SubregionRepository(BaseRepository):
    """The Subregion manager."""

    model = Subregion
    order_by: str = 'name'
    select_related: List[str] = ['region']
    prefetch_related: List[str] = ['alt_names']


class CityRepository(BaseRepository):
    """The City manager."""

    model = City
    order_by: str = 'name'
    select_related: List[str] = ['region', 'country', 'subregion']
    prefetch_related: List[str] = ['alt_names']


class DistrictRepository(BaseRepository):
    """The District manager."""

    model = District
    order_by: str = 'name'
    select_related: List[str] = ['city']
    prefetch_related: List[str] = ['alt_names']


class PostalCodeRepository(BaseRepository):
    """The PostalCode manager."""

    model = PostalCode
    order_by: str = 'id'
    select_related: List[str] = [
        'country',
        'region',
        'subregion',
        'city',
        'district',
        'city',
    ]
    prefetch_related: List[str] = ['alt_names']


class AlternativeNameRepository(BaseRepository):
    """The AlternativeName manager."""

    model = AlternativeName
    order_by: str = 'name'
    select_related: List[str] = []
    prefetch_related: List[str] = []
