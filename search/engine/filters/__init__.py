"""The search engine filters initialization module."""

from .abstract import Handler
from .country import CountryHandler
from .region import RegionHandler

__all__ = [
    "Handler",
    "CountryHandler",
    "RegionHandler",
]
