"""The admin tests module."""
from django.contrib import admin
from django.http.request import HttpRequest

from d8b.admin import (FieldsetFieldsUpdateMixin, ListDisplayUpdateMixin,
                       ListFilterUpdateMixin, ListLinksUpdateMixin,
                       SearchFieldsUpdateMixin)


class ModelMock():
    """The model mock."""

    _meta: None = None


class AdminMock(admin.ModelAdmin):
    """The admin mock."""

    list_display = ["l_one", "l_two"]
    search_fields = ["s_one", "s_two"]
    list_filter = ["f_one", "f_two"]
    list_display_links = ["link_one", "link_two"]
    fieldsets = [
        ("General", {
            "fields": ["fieldset_one", "fieldset_two", "fieldset_three"]
        }),
        ("Options", {
            "fields": ["created", "modified", "created_by", "modified_by"]
        }),
    ]


def test_fieldset_fields_update_mixin():
    """Should update admin fieldset fields."""

    class Test(AdminMock, FieldsetFieldsUpdateMixin):
        """The test class."""

        fieldsets_fields_extend = [
            "fieldset_three", "fieldset_four", "fieldset_five"
        ]
        fieldsets_fields_remove = ["fieldset_one", "fieldset_four"]

    obj = Test(ModelMock(), object())
    request = HttpRequest()
    assert obj.get_fieldsets(request, None)[0][1]["fields"] == [
        "fieldset_two", "fieldset_three", "fieldset_five"
    ]


def test_list_links_update_mixin():
    """Should update admin list links."""

    class Test(AdminMock, ListLinksUpdateMixin):
        """The test class."""

        list_links_extend = ["link_three", "link_four", "link_five"]
        list_links_remove = ["link_one", "link_four"]

    obj = Test(ModelMock(), object())
    request = HttpRequest()
    assert obj.get_list_display_links(
        request, None) == ["link_two", "link_three", "link_five"]


def test_search_fields_update_mixin():
    """Should update admin search fields."""

    class Test(AdminMock, SearchFieldsUpdateMixin):
        """The test class."""

        search_fields_extend = ["s_three", "s_four", "s_five"]
        search_fields_remove = ["s_one", "s_four"]

    obj = Test(ModelMock(), object())
    request = HttpRequest()
    assert obj.get_search_fields(request) == ["s_two", "s_three", "s_five"]


def test_list_filter_update_mixin():
    """Should update list filter fields."""

    class Test(AdminMock, ListFilterUpdateMixin):
        """The test class."""

        list_filter_extend = ["f_three", "f_four", "f_five"]
        list_filter_remove = ["f_one", "f_four"]

    obj = Test(ModelMock(), object())
    request = HttpRequest()
    assert obj.get_list_filter(request) == ["f_two", "f_three", "f_five"]


def test_list_display_update_mixin():
    """Should update list display fields."""

    class Test(AdminMock, ListDisplayUpdateMixin):
        """The test class."""

        list_display_extend = ["l_three", "l_four", "l_five"]
        list_display_remove = ["l_one", "l_four"]

    obj = Test(ModelMock(), object())
    request = HttpRequest()
    assert obj.get_list_display(request) == ["l_two", "l_three", "l_five"]
