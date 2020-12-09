"""The search engine filters initialization module."""

from .abstract import Handler
from .city import CityHandler
from .country import CountryHandler
from .dates import DatesHandler
from .district import DistrictHandler
from .postal_code import PostalCodeHandler
from .region import RegionHandler
from .subregion import SubregionHandler
from .tags import TagsHandler

__all__ = [
    "Handler",
    "CountryHandler",
    "RegionHandler",
    "SubregionHandler",
    "CityHandler",
    "DistrictHandler",
    "PostalCodeHandler",
    # "CoordinateHandler",
    "DatesHandler",
    "TagsHandler",

    # "RatingHandler",
    # "OnlyWithReviewsHandler",
    # "OnlyWithCertificatesHandler",
    # "ExperienceHandler"",
    # "GenderHandler"",
    # "AgeHandler"",
    # "ProfessionalLevelHandler"",
    # "LanguagesHandler"",
    # "NationalitiesHandler"",

    # "CategoriesHandler"",
    # "SubcategoriesHandler"",
    # "OnlyWithAutoOrderConfirmationHandler"",
    # "ServiceTypesHandler"",
    # "OnlyWithFixedPriceHandler"",
    # "StartPriceHandler"",
    # "EndPriceHandler"",
    # "PaymentMethodsHandler"",
    # "OnlyWithPhotosHandler"",
]
