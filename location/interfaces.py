"""The location interfaces module."""

from typing import Optional

from cities.models import (City, Country, District, PostalCode, Region,
                           Subregion)


class AbstractLocation():
    """The absctract location class."""

    country: Optional[Country]
    region: Optional[Region]
    subregion: Optional[Subregion]
    city: Optional[City]
    district: Optional[District]
    postal_code: Optional[PostalCode]
