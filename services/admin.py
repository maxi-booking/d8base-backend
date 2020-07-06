"""The services admin module."""
from typing import Tuple, Type

from django.contrib import admin
from imagekit.admin import AdminThumbnail
from reversion.admin import VersionAdmin

from .admin_fiters import ProfessionalFilter, ServiceFilter
from .models import Price, Service, ServiceLocation, ServicePhoto, ServiceTag


class ServiceTagInlineAdmin(admin.TabularInline):
    """The service tag admin class."""

    model = ServiceTag
    fields = ('id', 'name', 'created', 'modified', 'created_by', 'modified_by')
    readonly_fields = ('created', 'modified', 'created_by', 'modified_by')
    classes = ['collapse']
    extra = 3


class PriceInlineAdmin(admin.StackedInline):
    """The price admin class."""

    model = Price
    fields = ('id', 'price', 'is_price_fixed', 'start_price', 'end_price',
              'created', 'modified', 'created_by', 'modified_by')
    readonly_fields = ('created', 'modified', 'created_by', 'modified_by')


class ServiceLocationInlineAdmin(admin.TabularInline):
    """The price admin class."""

    model = ServiceLocation
    fields = ('id', 'location', 'max_distance', 'created', 'modified',
              'created_by', 'modified_by')
    readonly_fields = ('created', 'modified', 'created_by', 'modified_by')


@admin.register(ServicePhoto)
class ServicePhotoAdmin(VersionAdmin):
    """The service admin class."""

    model: Type = ServicePhoto
    photo_thumbnail = AdminThumbnail(image_field='photo_thumbnail')
    list_display = ('id', 'photo_thumbnail', 'name', 'order', 'created',
                    'created_by', 'service')
    list_display_links = ('id', 'name')
    list_filter = (ServiceFilter, )
    search_fields = ('=id', 'service__name', 'service__professional__name',
                     'name', 'description')
    readonly_fields = ('created', 'modified', 'created_by', 'modified_by')

    autocomplete_fields = ('service', )
    fieldsets: Tuple = (
        ('General', {
            'fields': ('name', 'description')
        }),
        ('Photo', {
            'fields': ('photo', )
        }),
        ('Options', {
            'fields': ('service', 'order', 'created', 'modified', 'created_by',
                       'modified_by')
        }),
    )
    list_select_related = ('service', 'service__professional',
                           'service__professional__user', 'created_by')

    class Media:
        """Required for the AutocompleteFilter."""


@admin.register(Service)
class ServiceAdmin(VersionAdmin):
    """The service admin class."""

    model: Type = Service
    list_display = ('id', 'name', 'duration', 'service_type', 'is_enabled',
                    'professional', 'created', 'modified')
    list_display_links = ('id', 'name')
    search_fields = ('=id', 'name', 'description', 'professional__name',
                     'professional__user__email')
    readonly_fields = ('created', 'modified', 'created_by', 'modified_by')
    list_filter = ('is_enabled', 'service_type', ProfessionalFilter)
    autocomplete_fields = ('professional', )
    inlines = (
        PriceInlineAdmin,
        ServiceTagInlineAdmin,
        ServiceLocationInlineAdmin,
    )

    fieldsets: Tuple = (
        ('General', {
            'fields': ('professional', 'name', 'description')
        }),
        ('Options', {
            'fields':
                ('duration', 'service_type', 'is_base_schedule', 'is_enabled',
                 'created', 'modified', 'created_by', 'modified_by')
        }),
    )
    list_select_related = ('professional', 'professional__user')

    class Media:
        """Required for the AutocompleteFilter."""
