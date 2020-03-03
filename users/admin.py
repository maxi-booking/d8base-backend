"""The users admin module."""

from typing import Any, List, Tuple, Type

from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _
from reversion.admin import VersionAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User

admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(VersionAdmin, BaseGroupAdmin):
    """The groups admin class."""


@admin.register(User)
class UserAdmin(VersionAdmin, BaseUserAdmin):
    """The users admin class."""

    add_form: Type = UserCreationForm
    form: Type = UserChangeForm
    model: Type = User

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

    def get_list_filter(self, request: HttpRequest) -> List[Any]:
        """Admin list filter."""
        list_display = list(super().get_list_filter(request))
        list_display.append('account_type')
        list_display.append('gender')
        return list_display

    def get_list_display(self, request: HttpRequest) -> List[Any]:
        """Admin list display."""
        list_display = list(super().get_list_display(request))
        list_display.remove('username')
        list_display.append('account_type')
        return list_display

    def get_search_fields(self, request: HttpRequest) -> List[Any]:
        """Admin search fields."""
        search_fields = list(super().get_search_fields(request))
        search_fields.remove('username')
        search_fields.append('patronymic')
        search_fields.append('phone')
        return search_fields
