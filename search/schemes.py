"""The search schemes module."""
from drf_yasg import openapi

from professionals.models import Professional
from search.engine.request import (HTTPToSearchLocationRequestConverter,
                                   HTTPToSearchProfessionalRequestConverter,
                                   HTTPToSearchRequestConverter,
                                   HTTPToSearchServiceRequestConverter)
from users.models import User

from .serializers import SearchSerializer


class SearchSchema():
    """The search schema."""

    list_schema = {
        "manual_parameters": [
            # SearchRequest
            openapi.Parameter(
                HTTPToSearchRequestConverter.QUERY_PARAM,
                openapi.IN_QUERY,
                description="search term query param",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                HTTPToSearchRequestConverter.START_DATETIME_PARAM,
                openapi.IN_QUERY,
                description="YYYY-MM-DDTHH:mm:ss (2020-08-23T16:19:43)",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                HTTPToSearchRequestConverter.END_DATETIME_PARAM,
                openapi.IN_QUERY,
                description="YYYY-MM-DDTHH:mm:ss (2020-08-23T16:19:43)",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                HTTPToSearchRequestConverter.TAGS_PARAM,
                openapi.IN_QUERY,
                description="multiple values may be separated by commas",
                type=openapi.TYPE_STRING,
            ),

            # SearchProfessionalRequest
            openapi.Parameter(
                HTTPToSearchProfessionalRequestConverter.RATING_PARAM,
                openapi.IN_QUERY,
                description="professional rating",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                HTTPToSearchProfessionalRequestConverter.
                ONLY_WITH_REVIEWS_PARAM,
                openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
            ),
            openapi.Parameter(
                HTTPToSearchProfessionalRequestConverter.
                ONLY_WITH_CERTIFICATES_PARAM,
                openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
            ),
            openapi.Parameter(
                HTTPToSearchProfessionalRequestConverter.EXPERIENCE_PARAM,
                openapi.IN_QUERY,
                description="professional experience",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                HTTPToSearchProfessionalRequestConverter.GENDER_PARAM,
                openapi.IN_QUERY,
                description=f"male: {User.GENDER_MALE}, \
                female: {User.GENDER_FEMALE}",
                type=openapi.TYPE_INTEGER,
                enum=[User.GENDER_MALE, User.GENDER_FEMALE],
            ),
            openapi.Parameter(
                HTTPToSearchProfessionalRequestConverter.START_AGE_PARAM,
                openapi.IN_QUERY,
                description="professional start age",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                HTTPToSearchProfessionalRequestConverter.END_AGE_PARAM,
                openapi.IN_QUERY,
                description="professional end age",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                HTTPToSearchProfessionalRequestConverter.
                PROFESSIONAL_LEVEL_PARAM,
                openapi.IN_QUERY,
                description="professional level",
                type=openapi.TYPE_STRING,
                enum=[
                    Professional.LEVEL_JUNIOR,
                    Professional.LEVEL_MIDDLE,
                    Professional.LEVEL_SENIOR,
                ],
            ),
            openapi.Parameter(
                HTTPToSearchProfessionalRequestConverter.LANGUAGES_PARAM,
                openapi.IN_QUERY,
                description="multiple values may be separated by commas",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                HTTPToSearchProfessionalRequestConverter.NATIONALITIES_PARAM,
                openapi.IN_QUERY,
                description="multiple country IDs may be separated by commas",
                type=openapi.TYPE_STRING,
            ),

            # SearchServiceRequest
            openapi.Parameter(
                HTTPToSearchServiceRequestConverter.CATEGORIES_PARAM,
                openapi.IN_QUERY,
                description="multiple category IDs may be separated by commas",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                HTTPToSearchServiceRequestConverter.SUBCATEGORIES_PARAM,
                openapi.IN_QUERY,
                description=
                "multiple subcategory IDs may be separated by commas",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                HTTPToSearchServiceRequestConverter.
                ONLY_WITH_AUTO_ORDER_CONFIRMATION_PARAM,
                openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
            ),
            openapi.Parameter(
                HTTPToSearchServiceRequestConverter.SERVICE_TYPES_PARAM,
                openapi.IN_QUERY,
                description="multiple types may be separated by commas",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                HTTPToSearchServiceRequestConverter.
                ONLY_WITH_FIXED_PRICE_PARAM,
                openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
            ),
            openapi.Parameter(
                HTTPToSearchServiceRequestConverter.START_PRICE_PARAM,
                openapi.IN_QUERY,
                description="start price value (12.35)",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                HTTPToSearchServiceRequestConverter.END_PRICE_PARAM,
                openapi.IN_QUERY,
                description="end price value (16.50)",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                HTTPToSearchServiceRequestConverter.PRICE_CURRENCY_PARAM,
                openapi.IN_QUERY,
                description="price currency (usd)",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                HTTPToSearchServiceRequestConverter.PAYMENT_METHODS_PARAM,
                openapi.IN_QUERY,
                description="multiple methods may be separated by commas",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                HTTPToSearchServiceRequestConverter.ONLY_WITH_PHOTOS_PARAM,
                openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
            ),

            # SearchLocationRequest
            openapi.Parameter(
                HTTPToSearchLocationRequestConverter.COUNTRY_PARAM,
                openapi.IN_QUERY,
                description="country ID",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                HTTPToSearchLocationRequestConverter.REGION_PARAM,
                openapi.IN_QUERY,
                description="region ID",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                HTTPToSearchLocationRequestConverter.SUBREGION_PARAM,
                openapi.IN_QUERY,
                description="subregion ID",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                HTTPToSearchLocationRequestConverter.CITY_PARAM,
                openapi.IN_QUERY,
                description="city ID",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                HTTPToSearchLocationRequestConverter.DISTRICT_PARAM,
                openapi.IN_QUERY,
                description="district ID",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                HTTPToSearchLocationRequestConverter.POSTAL_CODE_PARAM,
                openapi.IN_QUERY,
                description="postal code ID",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                HTTPToSearchLocationRequestConverter.COORDINATE_X_PARAM,
                openapi.IN_QUERY,
                description="longitude (-79.3849)",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                HTTPToSearchLocationRequestConverter.COORDINATE_Y_PARAM,
                openapi.IN_QUERY,
                description="latitude (43.6529)",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                HTTPToSearchLocationRequestConverter.MAX_DISTANCE_PARAM,
                openapi.IN_QUERY,
                description="max distance",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        "responses": {
            200: SearchSerializer(many=True)
        },
    }
