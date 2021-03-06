"""The location routers module."""
from rest_framework.routers import SimpleRouter

from .views import (AlternativeNameViewSet, CityViewSet, ContinentViewSet,
                    CountryViewSet, DistrictViewSet, ListLanguagesView,
                    PostalCodeViewSet, RegionViewSet, SubregionViewSet)


def get_router() -> SimpleRouter:
    """Return the app router."""
    router = SimpleRouter()
    router.register(r"location/languages", ListLanguagesView, "languages")
    router.register(r"location/continents", ContinentViewSet, "continents")
    router.register(r"location/countries", CountryViewSet, "countires")
    router.register(r"location/regions", RegionViewSet, "regions")
    router.register(r"location/subregions", SubregionViewSet, "subregions")
    router.register(r"location/cites", CityViewSet, "cities")
    router.register(r"location/districts", DistrictViewSet, "districts")
    router.register(r"location/postal-codes", PostalCodeViewSet,
                    "postal-codes")
    router.register(r"location/alternative-names", AlternativeNameViewSet,
                    "alternative-names")

    return router
