"""The users admin module."""

from typing import Tuple, Type

from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from reversion.admin import VersionAdmin

from d8b.admin import (ListDisplayUpdateMixin, ListFilterUpdateMixin,
                       SearchFieldsUpdateMixin)

from .forms import UserChangeForm, UserCreationForm
from .models import Language, User

admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(VersionAdmin, BaseGroupAdmin):
    """The groups admin class."""


class LanguageInlineAdmin(admin.TabularInline):
    """The languages inline admin."""

    model = Language
    fields = ('id', 'language', 'is_native', 'created', 'modified',
              'created_by', 'modified_by')
    fk_name = 'user'
    readonly_fields = ('created', 'modified', 'created_by', 'modified_by')


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

    inlines = (LanguageInlineAdmin, )

    fieldsets: Tuple = (
        (None, {
            'fields': ('email', 'password', 'account_type')
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

    list_display_extend = ['account_type']
    list_display_remove = ['username']
