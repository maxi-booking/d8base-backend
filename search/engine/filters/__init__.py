"""The search engine filters initialization module."""

from .abstract import Handler
from .city import CityHandler
from .country import CountryHandler
from .district import DistrictHandler
from .postal_code import PostalCodeHandler
from .region import RegionHandler
from .subregion import SubregionHandler

__all__ = [
    "Handler",
    "CountryHandler",
    "RegionHandler",
    "SubregionHandler",
    "CityHandler",
    "DistrictHandler",
    "PostalCodeHandler",
    # "CoordinateHandler",
]
