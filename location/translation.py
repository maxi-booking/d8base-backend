"""The location translation module."""

from cities.models import City, Continent, Country, District, Region, Subregion
from modeltranslation.translator import TranslationOptions, register


@register(Continent)
class ContinentTranslationOptions(TranslationOptions):
    """The continent translation options class."""

    fields = ("name", )
    required_languages = ("en", )


@register(Country)
class CountryTranslationOptions(TranslationOptions):
    """The country translation options class."""

    fields = ("name", )
    required_languages = ("en", )


@register(Region)
class RegionTranslationOptions(TranslationOptions):
    """The region translation options class."""

    fields = ("name", "name_std")
    required_languages = ("en", )


@register(Subregion)
class SubregionTranslationOptions(TranslationOptions):
    """The subregion translation options class."""

    fields = ("name", "name_std")
    required_languages = ("en", )


@register(City)
class CityTranslationOptions(TranslationOptions):
    """The city translation options class."""

    fields = ("name", "name_std")
    required_languages = ("en", )


@register(District)
class DistrictTranslationOptions(TranslationOptions):
    """The district translation options class."""

    fields = ("name", "name_std")
    required_languages = ("en", )
