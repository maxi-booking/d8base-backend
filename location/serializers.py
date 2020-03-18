"""The location serializers module."""
from cities.models import (AlternativeName, City, Continent, Country, District,
                           PostalCode, Region, Subregion)
from rest_framework import serializers


class ContinentSerializer(serializers.ModelSerializer):
    """The Continent class serializer."""

    class Meta:
        """The Continent class serializer META class."""

        model = Continent
        fields = ['id', 'slug', 'name', 'alt_names', 'code']


class CountrySerializer(serializers.ModelSerializer):
    """The Country class serializer."""

    class Meta:
        """The Country class serializer META class."""

        model = Country
        fields = [
            'id', 'slug', 'name', 'alt_names', 'code', 'code3', 'population',
            'area', 'currency', 'currency_name', 'currency_symbol',
            'language_codes', 'phone', 'continent', 'tld',
            'postal_code_format', 'postal_code_regex', 'capital', 'neighbours'
        ]


class RegionSerializer(serializers.ModelSerializer):
    """The Region class serializer."""

    class Meta:
        """The Region class serializer META class."""

        model = Region
        fields = [
            'id', 'slug', 'name', 'name_std', 'alt_names', 'code', 'country'
        ]


class SubregionSerializer(serializers.ModelSerializer):
    """The Subregion class serializer."""

    class Meta:
        """The Subregion class serializer META class."""

        model = Subregion
        fields = [
            'id', 'slug', 'name', 'name_std', 'alt_names', 'code', 'region'
        ]


class CitySerializer(serializers.ModelSerializer):
    """The City class serializer."""

    class Meta:
        """The City class serializer META class."""

        model = City
        fields = [
            'id', 'slug', 'name', 'name_std', 'alt_names', 'country', 'region',
            'subregion', 'location', 'population', 'elevation', 'kind',
            'timezone'
        ]


class DistrictSerializer(serializers.ModelSerializer):
    """The District class serializer."""

    class Meta:
        """The District class serializer META class."""

        model = District

        fields = [
            'id', 'slug', 'name', 'name_std', 'alt_names', 'code', 'location',
            'population', 'city'
        ]


class PostalCodeSerializer(serializers.ModelSerializer):
    """The PostalCode class serializer."""

    class Meta:
        """The PostalCode class serializer META class."""

        model = PostalCode

        fields = [
            'id', 'slug', 'name', 'alt_names', 'code', 'region_name',
            'subregion_name', 'district_name', 'country', 'region',
            'subregion', 'city', 'district', 'names', 'name_full'
        ]


class AlternativeNameSerializer(serializers.ModelSerializer):
    """The AlternativeName class serializer."""

    class Meta:
        """The AlternativeName class serializer META class."""

        model = AlternativeName
        fields = [
            'id', 'slug', 'name', 'kind', 'language_code', 'is_preferred',
            'is_short', 'is_colloquial', 'is_historic'
        ]


class LanguageSerializer(serializers.Serializer):
    """The language class serializer."""

    # pylint: disable=abstract-method
    code = serializers.CharField(max_length=2)
    name = serializers.CharField(max_length=200)
