"""The location interfaces module."""

from dataclasses import dataclass
from typing import Optional

from cities.models import (City, Country, District, PostalCode, Region,
                           Subregion)


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
