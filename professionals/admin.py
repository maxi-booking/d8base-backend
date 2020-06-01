"""The professionals admin module."""

from typing import Tuple, Type

from adminsortable.admin import SortableAdmin, SortableTabularInline
from django.contrib import admin
from imagekit.admin import AdminThumbnail
from modeltranslation.admin import (TabbedTranslationAdmin,
                                    TranslationTabularInline)
from reversion.admin import VersionAdmin

from location.admin_filters import CityFilter, DistrictFilter, RegionFilter
from users.admin_fiters import UserFilter

from .admin_fiters import ProfessionalFilter
from .models import (Category, Professional, ProfessionalCertificate,
                     ProfessionalContact, ProfessionalEducation,
                     ProfessionalExperience, ProfessionalLocation,
                     ProfessionalPhoto, ProfessionalTag, Subcategory)


class SubcategoryInlineAdmin(SortableTabularInline, TranslationTabularInline):
    """The subcategories admin class."""

    model = Subcategory
    fields = ('id', 'name', 'description', 'created', 'modified', 'created_by',
              'modified_by')
    readonly_fields = ('created', 'modified', 'created_by', 'modified_by')
    extra = 3


@admin.register(Category)
class CategoryAdmin(SortableAdmin, VersionAdmin, TabbedTranslationAdmin):
    """The categories admin class."""

    model: Type = Category
    list_display = ('id', 'name', 'created', 'created_by')
    search_fields = ('=id', 'name')
    readonly_fields = ('created', 'modified', 'created_by', 'modified_by')
    change_list_template_extends = 'reversion/change_list.html'

    inlines = (SubcategoryInlineAdmin, )

    fieldsets: Tuple = (
        ('General', {
            'fields': ('name', 'description')
        }),
        ('Options', {
            'fields': ('created', 'modified', 'created_by', 'modified_by')
        }),
    )
    list_select_related = ('created_by', )


class ProfessionalTagInlineAdmin(admin.TabularInline):
    """The subcategories admin class."""

    model = ProfessionalTag
    fields = ('id', 'name', 'created', 'modified', 'created_by', 'modified_by')
    readonly_fields = ('created', 'modified', 'created_by', 'modified_by')
    classes = ['collapse']
    extra = 3


class ProfessionalContactInlineAdmin(admin.TabularInline):
    """The professional contact admin class."""

    model = ProfessionalContact
    fields = ('id', 'contact', 'value', 'created', 'modified', 'created_by',
              'modified_by')
    readonly_fields = ('created', 'modified', 'created_by', 'modified_by')
    autocomplete_fields = ('contact', )
    classes = ['collapse']
    extra = 1


class ProfessionalLocationInlineAdmin(admin.StackedInline):
    """The location inline admin."""

    model = ProfessionalLocation
    fields = ('id', 'user_location', 'country', 'region', 'subregion', 'city',
              'district', 'postal_code', 'address', 'coordinates',
              'is_default', 'timezone', 'units', 'created_by', 'modified_by')
    readonly_fields = ('created', 'modified', 'created_by', 'modified_by')
    autocomplete_fields = ('region', 'user_location', 'subregion', 'city',
                           'district', 'postal_code')
    classes = ['collapse']
    extra = 1


class ProfessionalEducationInlineAdmin(admin.StackedInline):
    """The education inline admin."""

    model = ProfessionalEducation
    fields = ('id', 'university', 'deegree', 'field_of_study', 'is_still_here',
              'start_date', 'end_date', 'description', 'created_by',
              'modified_by')
    readonly_fields = ('created', 'modified', 'created_by', 'modified_by')
    classes = ['collapse']
    extra = 1


class ProfessionalExperienceInlineAdmin(admin.StackedInline):
    """The experience inline admin."""

    model = ProfessionalExperience
    fields = ('id', 'title', 'company', 'is_still_here', 'start_date',
              'end_date', 'description', 'created_by', 'modified_by')
    readonly_fields = ('created', 'modified', 'created_by', 'modified_by')
    classes = ['collapse']
    extra = 1


class ProfessionalCertificateInlineAdmin(admin.StackedInline):
    """The certificate inline admin."""

    model = ProfessionalCertificate
    fields = ('id', 'name', 'organization', 'date', 'certificate_id', 'url',
              'photo', 'created_by', 'modified_by')
    readonly_fields = ('created', 'modified', 'created_by', 'modified_by')
    classes = ['collapse']
    extra = 1


@admin.register(Professional)
class ProfessionalAdmin(VersionAdmin):
    """The professional admin class."""

    model: Type = Professional
    list_display = ('id', 'name', 'slug', 'rating', 'subcategory', 'level',
                    'experience', 'user', 'created_by')
    list_display_links = ('id', 'name')
    search_fields = ('=id', 'name', 'user__email', 'user__last_name')
    readonly_fields = ('rating', 'created', 'modified', 'created_by',
                       'modified_by')
    list_filter = ('level', 'subcategory', UserFilter)
    autocomplete_fields = ('user', )
    inlines = (
        ProfessionalTagInlineAdmin,
        ProfessionalContactInlineAdmin,
        ProfessionalLocationInlineAdmin,
        ProfessionalEducationInlineAdmin,
        ProfessionalExperienceInlineAdmin,
        ProfessionalCertificateInlineAdmin,
    )

    fieldsets: Tuple = (
        ('General', {
            'fields': ('name', 'description', 'company', 'subcategory')
        }),
        ('Experience', {
            'fields': ('experience', 'level', 'rating')
        }),
        ('Options', {
            'fields': ('is_auto_order_confirmation', 'slug', 'user', 'created',
                       'modified', 'created_by', 'modified_by')
        }),
    )
    list_select_related = ('created_by', 'subcategory', 'user')

    class Media:
        """Required for the AutocompleteFilter."""


@admin.register(ProfessionalEducation)
class ProfessionalEducationAdmin(VersionAdmin):
    """The education admin class."""

    model: Type = ProfessionalEducation
    list_display = ('id', 'professional', 'university', 'deegree',
                    'start_date', 'end_date', 'created', 'created_by')
    list_display_links = ('id', 'professional')
    list_filter = (ProfessionalFilter, )
    search_fields = ('=id', 'professional__name', 'professional__user__email',
                     'university', 'description')
    readonly_fields = ('created', 'modified', 'created_by', 'modified_by')

    autocomplete_fields = ('professional', )
    fieldsets: Tuple = (
        ('General', {
            'fields':
                ('university', 'deegree', 'field_of_study', 'description')
        }),
        ('Dates', {
            'fields': ('is_still_here', 'start_date', 'end_date')
        }),
        ('Options', {
            'fields': ('professional', 'created', 'modified', 'created_by',
                       'modified_by')
        }),
    )
    list_select_related = ('professional', 'professional__user', 'created_by')

    class Media:
        """Required for the AutocompleteFilter."""


@admin.register(ProfessionalExperience)
class ProfessionalExperienceAdmin(VersionAdmin):
    """The experience admin class."""

    model: Type = ProfessionalExperience
    list_display = ('id', 'professional', 'title', 'company', 'start_date',
                    'end_date', 'created', 'created_by')
    list_display_links = ('id', 'professional')
    list_filter = (ProfessionalFilter, )
    search_fields = ('=id', 'professional__name', 'professional__user__email',
                     'title', 'company')
    readonly_fields = ('created', 'modified', 'created_by', 'modified_by')

    autocomplete_fields = ('professional', )
    fieldsets: Tuple = (
        ('General', {
            'fields': ('title', 'company', 'description')
        }),
        ('Dates', {
            'fields': ('is_still_here', 'start_date', 'end_date')
        }),
        ('Options', {
            'fields': ('professional', 'created', 'modified', 'created_by',
                       'modified_by')
        }),
    )
    list_select_related = ('professional', 'professional__user', 'created_by')

    class Media:
        """Required for the AutocompleteFilter."""


@admin.register(ProfessionalCertificate)
class ProfessionalCertificateAdmin(VersionAdmin):
    """The certificate admin class."""

    model: Type = ProfessionalCertificate
    list_display = ('id', 'professional', 'name', 'organization', 'date',
                    'created', 'created_by')
    list_display_links = ('id', 'professional')
    list_filter = (ProfessionalFilter, )
    search_fields = ('=id', 'professional__name', 'professional__user__email',
                     'name', 'organization')
    readonly_fields = ('created', 'modified', 'created_by', 'modified_by')

    autocomplete_fields = ('professional', )
    fieldsets: Tuple = (
        ('General', {
            'fields': ('name', 'organization', 'date')
        }),
        ('Certificate', {
            'fields': ('certificate_id', 'url', 'photo')
        }),
        ('Options', {
            'fields': ('professional', 'created', 'modified', 'created_by',
                       'modified_by')
        }),
    )
    list_select_related = ('professional', 'professional__user', 'created_by')

    class Media:
        """Required for the AutocompleteFilter."""


@admin.register(ProfessionalPhoto)
class ProfessionalPhotoAdmin(VersionAdmin):
    """The photo admin class."""

    model: Type = ProfessionalPhoto
    photo_thumbnail = AdminThumbnail(image_field='photo_thumbnail')
    list_display = ('id', 'photo_thumbnail', 'name', 'order', 'created',
                    'created_by')
    list_display_links = ('id', 'name')
    list_filter = (ProfessionalFilter, )
    search_fields = ('=id', 'professional__name', 'professional__user__email',
                     'name', 'description')
    readonly_fields = ('created', 'modified', 'created_by', 'modified_by')

    autocomplete_fields = ('professional', )
    fieldsets: Tuple = (
        ('General', {
            'fields': ('name', 'description')
        }),
        ('Photo', {
            'fields': ('photo', )
        }),
        ('Options', {
            'fields': ('professional', 'order', 'created', 'modified',
                       'created_by', 'modified_by')
        }),
    )
    list_select_related = ('professional', 'professional__user', 'created_by')

    class Media:
        """Required for the AutocompleteFilter."""


@admin.register(ProfessionalLocation)
class ProfessionalLocationAdmin(VersionAdmin):
    """The location admin class."""

    model: Type = ProfessionalLocation
    list_display = ('id', 'professional', 'country', 'region', 'city',
                    'district', 'coordinates', 'created', 'created_by')
    list_display_links = ('id', 'professional')
    list_filter = (
        'country',
        RegionFilter,
        CityFilter,
        DistrictFilter,
        ProfessionalFilter,
    )
    search_fields = ('=id', 'professional__name', 'professional__user__email',
                     'country__name', 'region__name', 'city__name', 'address')
    readonly_fields = ('created', 'modified', 'created_by', 'modified_by')

    autocomplete_fields = ('professional', 'region', 'subregion', 'city',
                           'district', 'postal_code', 'user_location')
    fieldsets: Tuple = (
        ('General', {
            'fields': ('country', 'region', 'subregion', 'city', 'district',
                       'postal_code', 'address', 'coordinates')
        }),
        ('Options', {
            'fields': ('professional', 'user_location', 'units', 'timezone',
                       'created', 'modified', 'created_by', 'modified_by')
        }),
    )
    list_select_related = ('professional', 'professional__user', 'country',
                           'region', 'city', 'district', 'created_by')

    class Media:
        """Required for the AutocompleteFilter."""
