"""The professionals services module."""
from typing import TYPE_CHECKING, List, Optional

from communication.models import Review
from location.interfaces import AbstractLocation, BaseLocationAutofiller

if TYPE_CHECKING:
    from .models import Professional


class LocationCopyAutofiller(BaseLocationAutofiller):
    """The location copy autofiller."""

    destination: AbstractLocation
    source: Optional[AbstractLocation]

    members: List[str] = [
        'postal_code', 'district', 'city', 'subregion', 'region', 'country',
        'units', 'coordinates', 'address', 'timezone'
    ]

    def __init__(self, destination: AbstractLocation,
                 source: Optional[AbstractLocation]):
        """Construct the object."""
        self.source = source
        self.destination = destination

    def _copy_value(self, name: str) -> None:
        """Copy a value from the source to the destination."""
        source_value = getattr(self.source, name)
        setattr(self.destination, name, source_value)

    def autofill_location(self) -> AbstractLocation:
        """Autofill a location object fields."""
        if not self.source:
            return self.destination

        for name in self.members:
            self._copy_value(name)

        return self.destination


# TODO: Test it
def update_professional_rating(professional: 'Professional'):
    """Update the professional rating."""
    rating = Review.objects.get_professional_rating(professional)
    professional.rating = rating
    professional.save()
