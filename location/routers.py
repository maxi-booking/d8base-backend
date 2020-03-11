"""The location models module."""
from rest_framework.routers import SimpleRouter

from .views import (AlternativeNameViewSet, CityViewSet, ContinentViewSet,
                    CountryViewSet, DistrictViewSet, PostalCodeViewSet,
                    RegionViewSet, SubregionViewSet)


def get_router() -> SimpleRouter:
    """Return the app router."""
    router = SimpleRouter()
    router.register(r'location/continents', ContinentViewSet, 'continents')
    router.register(r'location/countires', CountryViewSet, 'countires')
    router.register(r'location/regions', RegionViewSet, 'regions')
    router.register(r'location/subregions', SubregionViewSet, 'subregions')
    router.register(r'location/cites', CityViewSet, 'cities')
    router.register(r'location/districts', DistrictViewSet, 'districts')
    router.register(r'location/postal-codes', PostalCodeViewSet,
                    'postal_codes')
    router.register(r'location/alternative-names', AlternativeNameViewSet,
                    'alternative_names')

    return router
