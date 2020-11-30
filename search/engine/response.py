"""The search response module."""
from typing import List

from professionals.models import Professional
from services.models import Service


class SearchResponse():
    """The search request class."""

    professional: Professional
    services: List[Service]
