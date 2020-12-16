"""The location admin module."""
from cities import admin as base_admin
from cities import models as base_models
from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from reversion.admin import VersionAdmin

from d8b.admin import SearchFieldsUpdateMixin

admin.site.unregister(base_models.Continent)
admin.site.unregister(base_models.Country)
admin.site.unregister(base_models.Region)
admin.site.unregister(base_models.Subregion)
admin.site.unregister(base_models.City)
admin.site.unregister(base_models.District)
admin.site.unregister(base_models.AlternativeName)
admin.site.unregister(base_models.PostalCode)


@admin.register(base_models.Continent)
class ContinentAdmin(VersionAdmin, base_admin.ContinentAdmin):
    """The continent admin."""


@admin.register(base_models.Country)
class CountryAdmin(
        VersionAdmin,
        base_admin.CountryAdmin,
        SearchFieldsUpdateMixin,
        TabbedTranslationAdmin,
):
    """The country admin."""

    list_filter = ("continent", )
    list_select_related = ("continent", )
    search_fields_extend = ["continent__name"]


@admin.register(base_models.Region)
class RegionAdmin(
        VersionAdmin,
        base_admin.RegionAdmin,
        SearchFieldsUpdateMixin,
        TabbedTranslationAdmin,
):
    """The region admin."""

    list_select_related = ("country", )
    search_fields_extend = ["country__name"]
    autocomplete_fields = ("alt_names", )


@admin.register(base_models.Subregion)
class SubregionAdmin(
        VersionAdmin,
        base_admin.SubregionAdmin,
        SearchFieldsUpdateMixin,
        TabbedTranslationAdmin,
):
    """The subregion admin."""

    list_select_related = ("region", )
    search_fields_extend = ["region__name", "region__country__name"]
    autocomplete_fields = ("alt_names", "region")


@admin.register(base_models.City)
class CitiesAdmin(
        VersionAdmin,
        base_admin.CityAdmin,
        SearchFieldsUpdateMixin,
        TabbedTranslationAdmin,
):
    """The cities admin."""

    list_filter = ("country", )
    list_select_related = ("country", "region", "subregion")
    search_fields_extend = ["country__name", "region__name", "subregion__name"]
    autocomplete_fields = ("alt_names", "region", "subregion")


@admin.register(base_models.District)
class DistrictAdmin(
        VersionAdmin,
        base_admin.DistrictAdmin,
        SearchFieldsUpdateMixin,
        TabbedTranslationAdmin,
):
    """The district admin."""

    list_select_related = ("city", )
    search_fields_extend = ["city__name"]
    autocomplete_fields = ("alt_names", "city")


@admin.register(base_models.AlternativeName)
class AlternativeNameAdmin(VersionAdmin, base_admin.AltNameAdmin):
    """The alternative name admin."""


@admin.register(base_models.PostalCode)
class PostalCodeAdmin(
        VersionAdmin,
        base_admin.PostalCodeAdmin,
        SearchFieldsUpdateMixin,
):
    """The alternative name admin."""

    autocomplete_fields = [
        "alt_names", "region", "subregion", "city", "district"
    ]
    list_select_related = ("subregion", "region", "country")
    search_fields_extend = [
        "region__name", "subregion__name", "city__name", "district__name"
    ]
