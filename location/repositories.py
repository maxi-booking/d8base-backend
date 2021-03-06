"""The location repositories module."""

from abc import ABC, abstractmethod
from typing import List, Optional, Type

from cities.models import (AlternativeName, City, Continent, Country, District,
                           Place, PostalCode, Region, Subregion)
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models.query import QuerySet

from d8b.trans import translate

from .documents import CityDocument
from .models import Language


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

    def get_to_translate(self, lang: str) -> QuerySet:
        """Return a list of objects to translate."""
        return self.get_list().filter(**{f"name_{lang}__isnull": True})

    @staticmethod
    def translate(obj, lang: str):
        """Translate the cities object."""
        translation = translate(obj.name, src="en", dest=lang)
        if translation:
            setattr(obj, f"name_{lang}", translation)
        obj.save()


class ContinentRepository(BaseRepository):
    """The Continent repository."""

    model = Continent
    order_by: str = "name"
    select_related: List[str] = []
    prefetch_related: List[str] = ["alt_names"]


class CountryRepository(BaseRepository):
    """The Country repository."""

    model = Country
    order_by: str = "name"
    select_related: List[str] = ["continent"]
    prefetch_related: List[str] = ["neighbours", "alt_names"]

    @staticmethod
    def get_language(country: Country) -> Optional[str]:
        """Return the country language."""
        codes = country.language_codes
        if not codes:
            return None
        return codes.split(",")[0].split("-")[0].strip().lower()


class RegionRepository(BaseRepository):
    """The Region repository."""

    model = Region
    order_by: str = "name"
    select_related: List[str] = ["country"]
    prefetch_related: List[str] = ["alt_names"]


class SubregionRepository(BaseRepository):
    """The Subregion repository."""

    model = Subregion
    order_by: str = "name"
    select_related: List[str] = ["region"]
    prefetch_related: List[str] = ["alt_names"]


class CityRepository(BaseRepository):
    """The City repository."""

    model = City
    order_by: str = "name"
    select_related: List[str] = ["region", "country", "subregion"]
    prefetch_related: List[str] = ["alt_names"]

    def find_by_name(
        self,
        *,
        name: str,
        queryset: Optional[QuerySet] = None,
    ) -> QuerySet:
        """Find cities by the name."""
        if queryset is None:
            queryset = self.get_list()
        result = CityDocument.search().query(
            "query_string", query=f"{name}*")[:settings.D8B_SEARCH_MAX_ENTRIES]
        ids = {r.meta.id for r in result}

        return queryset.filter(pk__in=ids)


class DistrictRepository(BaseRepository):
    """The District repository."""

    model = District
    order_by: str = "name"
    select_related: List[str] = ["city"]
    prefetch_related: List[str] = ["alt_names"]


class PostalCodeRepository(BaseRepository):
    """The PostalCode repository."""

    model = PostalCode
    order_by: str = "id"
    select_related: List[str] = [
        "country",
        "region",
        "subregion",
        "city",
        "district",
        "city",
    ]
    prefetch_related: List[str] = ["alt_names"]

    @staticmethod
    def find_by_city(
        *,
        city_id: int,
        queryset: QuerySet,
    ) -> QuerySet:
        """Find postal codes by the city."""
        return queryset.filter(Q(city__pk=city_id) | Q(city__isnull=True))


class AlternativeNameRepository(BaseRepository):
    """The AlternativeName repository."""

    model = AlternativeName
    order_by: str = "name"
    select_related: List[str] = []
    prefetch_related: List[str] = []


class LanguageRepository():
    """The language repository."""

    languages = settings.LANGUAGES

    def get_list(self) -> List[Language]:
        """Return the list of languages."""
        return [Language(r[0], r[1]) for r in self.languages]

    def get(self, code: str) -> Language:
        """Return a languages object."""
        for lang in self.languages:
            if lang[0] == code:
                return Language(lang[0], lang[1])
        raise ObjectDoesNotExist
