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
from .models import (User, UserContact, UserLanguage, UserLocation,
                     UserSavedProfessional, UserSettings)

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
            'fields': ('user', 'units', 'timezone', 'is_default', 'created',
                       'modified', 'created_by', 'modified_by')
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
              'timezone', 'units', 'created_by', 'modified_by')
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


@admin.register(UserContact)
class UserContactAdmin(admin.ModelAdmin):
    """The user contacts admin."""

    model: Type = UserContact
    list_display = ('id', 'contact', 'value', 'user', 'created_by')
    list_display_links = ('id', 'contact')
    search_fields = ('=id', 'contact', 'user__email', 'user__last_name')
    readonly_fields = ('created', 'modified', 'created_by', 'modified_by')
    list_filter = ('contact', UserFilter)
    autocomplete_fields = ('user', 'contact')

    fieldsets: Tuple = (
        ('General', {
            'fields': (
                'contact',
                'value',
            )
        }),
        ('Options', {
            'fields':
                ('user', 'created', 'modified', 'created_by', 'modified_by')
        }),
    )
    list_select_related = ('created_by', 'user', 'contact')

    class Media:
        """Required for the AutocompleteFilter."""


class ContactInlineAdmin(admin.TabularInline):
    """The contacts inline admin."""

    model = UserContact
    fk_name = 'user'
    fields = ('id', 'contact', 'value', 'created', 'modified', 'created_by',
              'modified_by')
    readonly_fields = ('created', 'modified', 'created_by', 'modified_by')
    autocomplete_fields = ('contact', )
    classes = ['collapse']
    extra = 1


class SettingsInlineAdmin(admin.TabularInline):
    """The setting inline admin."""

    model = UserSettings
    fk_name = 'user'
    fields = ('id', 'language', 'currency', 'units', 'is_last_name_hidden',
              'created', 'modified', 'created_by', 'modified_by')
    readonly_fields = ('created', 'modified', 'created_by', 'modified_by')
    classes = ['collapse']


class SavedProfessionlInlineAdmin(admin.TabularInline):
    """The saved professional inline admin."""

    model = UserSavedProfessional
    fk_name = 'user'
    fields = ('id', 'professional', 'note', 'created', 'modified',
              'created_by', 'modified_by')
    readonly_fields = ('created', 'modified', 'created_by', 'modified_by')
    extra = 1
    classes = ['collapse']


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
    inlines = (
        LanguageInlineAdmin,
        LocationInlineAdmin,
        ContactInlineAdmin,
        SettingsInlineAdmin,
        SavedProfessionlInlineAdmin,
    )

    avatar_thumbnail = AdminThumbnail(image_field='avatar_thumbnail')

    fieldsets: Tuple = (
        (None, {
            'fields': ('email', 'password', 'account_type', 'avatar')
        }),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'patronymic', 'gender',
                       'birthday', 'nationality', 'phone')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_confirmed', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions'),
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

    list_filter_extend = ['account_type', 'is_confirmed', 'gender']

    list_display_extend = ['account_type', 'is_confirmed', 'avatar_thumbnail']
    list_display_remove = ['username']
