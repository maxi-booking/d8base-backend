"""The location interfaces module."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from cities.models import (City, Country, District, PostalCode, Region,
                           Subregion)
from django.contrib.gis.geos import Point


@dataclass
class AbstractLocation():
    """The absctract location class."""

    country: Optional[Country] = None
    region: Optional[Region] = None
    subregion: Optional[Subregion] = None
    city: Optional[City] = None
    district: Optional[District] = None
    postal_code: Optional[PostalCode] = None
    timezone: Optional[str] = None
    units: int = 0
    address: Optional[str] = None
    coordinates: Optional[Point] = None


class BaseLocationAutofiller(ABC):
    """The base location autofiller."""

    @abstractmethod
    def autofill_location(self) -> AbstractLocation:
        """Autofill the location."""
