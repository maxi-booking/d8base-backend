"""The users admin module."""

from typing import Tuple, Type

from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from imagekit.admin import AdminThumbnail
from oauth2_provider.admin import ApplicationAdmin
from oauth2_provider.models import Application
from reversion.admin import VersionAdmin

from d8b.admin import (ListDisplayUpdateMixin, ListFilterUpdateMixin,
                       SearchFieldsUpdateMixin)
from location.admin_filters import CityFilter, DistrictFilter, RegionFilter

from .admin_fiters import UserFilter
from .forms import UserChangeForm, UserCreationForm
from .models import User, UserLanguage, UserLocation

admin.site.unregister(Application)


@admin.register(Application)
class OauthApplicationAdmin(VersionAdmin, ApplicationAdmin):
    """The groups admin class."""


admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(VersionAdmin, BaseGroupAdmin):
    """The groups admin class."""


@admin.register(UserLocation)
class LocationAdmin(VersionAdmin):
    """The location admin class."""

    model: Type = UserLocation
    list_display = ('id', 'user', 'is_default', 'country', 'region', 'city',
                    'district', 'coordinates', 'created', 'created_by')
    list_filter = (
        'country',
        RegionFilter,
        CityFilter,
        DistrictFilter,
        UserFilter,
        'is_default',
    )
    search_fields = ('=id', 'user__email', 'country__name', 'region__name',
                     'city__name', 'address')
    readonly_fields = ('created', 'modified', 'created_by', 'modified_by')

    autocomplete_fields = ('user', 'region', 'subregion', 'city', 'district',
                           'postal_code')
    fieldsets: Tuple = (
        ('General', {
            'fields': ('country', 'region', 'subregion', 'city', 'district',
                       'postal_code', 'address', 'coordinates')
        }),
        ('Options', {
            'fields': ('user', 'is_default', 'created', 'modified',
                       'created_by', 'modified_by')
        }),
    )
    list_select_related = ('user', 'country', 'region', 'city', 'district',
                           'created_by')

    class Media:
        """Required for the AutocompleteFilter."""


class LocationInlineAdmin(admin.StackedInline):
    """The location inline admin."""

    model = UserLocation
    fk_name = 'user'
    fields = ('id', 'country', 'region', 'subregion', 'city', 'district',
              'postal_code', 'address', 'coordinates', 'is_default',
              'created_by', 'modified_by')
    readonly_fields = ('created', 'modified', 'created_by', 'modified_by')
    autocomplete_fields = ('region', 'subregion', 'city', 'district',
                           'postal_code')
    classes = ['collapse']
    extra = 1


class LanguageInlineAdmin(admin.TabularInline):
    """The languages inline admin."""

    model = UserLanguage
    fk_name = 'user'
    fields = ('id', 'language', 'is_native', 'created', 'modified',
              'created_by', 'modified_by')
    readonly_fields = ('created', 'modified', 'created_by', 'modified_by')
    classes = ['collapse']
    extra = 1


@admin.register(User)
class UserAdmin(
        VersionAdmin,
        BaseUserAdmin,
        SearchFieldsUpdateMixin,
        ListFilterUpdateMixin,
        ListDisplayUpdateMixin,
):
    """The users admin class."""

    add_form: Type = UserCreationForm
    form: Type = UserChangeForm
    model: Type = User
    inlines = (LanguageInlineAdmin, LocationInlineAdmin)

    avatar_thumbnail = AdminThumbnail(image_field='avatar_thumbnail')

    fieldsets: Tuple = (
        (None, {
            'fields': ('email', 'password', 'account_type', 'avatar')
        }),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'patronymic', 'gender',
                       'birthday', 'phone')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',
                       'user_permissions'),
        }),
        (_('Dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )
    add_fieldsets: Tuple = ((None, {
        'classes': ('wide', ),
        'fields': ('email', 'password1', 'password2'),
    }), )

    ordering = ('email', )

    search_fields_extend = ['patronymic', 'phone']
    search_fields_remove = ['username']

    list_filter_extend = ['account_type', 'gender']

    list_display_extend = ['account_type', 'avatar_thumbnail']
    list_display_remove = ['username']
