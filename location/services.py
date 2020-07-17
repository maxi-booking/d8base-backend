"""The location services module."""
from typing import List

from cities.models import City, District, PostalCode, Region, Subregion
from django.conf import settings

from .interfaces import AbstractLocation, BaseLocationAutofiller


class LocationAutofiller(BaseLocationAutofiller):
    """The location autofiller."""

    location: AbstractLocation

    members: List[str] = [
        "postal_code", "district", "city", "subregion", "region"
    ]

    def __init__(self, location: AbstractLocation):
        """Construct the object."""
        self.location = location

    def _set_from_postal_code(self):
        """Set from the postal_code."""
        source: PostalCode = self.location.postal_code
        self.location.district = source.district
        self.location.city = source.city
        self.location.subregion = source.subregion
        self.location.region = source.region
        self.location.country = source.country

    def _set_from_district(self):
        """Set from the district."""
        source: District = self.location.district
        self.location.city = source.city
        self.location.subregion = source.city.subregion
        self.location.region = source.city.region
        self.location.country = source.city.country

    def _set_from_city(self):
        """Set from the city."""
        source: City = self.location.city
        self.location.subregion = source.subregion
        self.location.region = source.region
        self.location.country = source.country

    def _set_from_subregion(self):
        """Set from the subregion."""
        source: Subregion = self.location.subregion
        self.location.region = source.region
        self.location.country = source.region.country

    def _set_from_region(self):
        """Set from the city."""
        source: Region = self.location.region
        self.location.country = source.country

    def _set_timezone(self):
        """Set the timezone attr based on the city attr."""
        city = getattr(self.location, "city", None)
        if city and city.timezone:
            self.location.timezone = city.timezone

    def _set_units(self):
        """Set the units based on the country attr."""
        country = getattr(self.location, "country", None)
        if not country:
            return
        if country.tld in settings.IMPERIAL_UNITS_COUNTRIES:
            self.location.units = settings.UNITS_IMPERIAL

    def autofill_location(self) -> AbstractLocation:
        """Autofill a location object fields."""
        self._set_units()
        for member in self.members:
            if getattr(self.location, member, None):
                getattr(self, f"_set_from_{member}")()
                self._set_timezone()
                return self.location

        return self.location
