"""The models tests module."""
import pytest
from django.test.client import Client
from django.urls import reverse

import d8b.middleware
from d8b.models import CommonInfo
from users.models import User

pytestmark = pytest.mark.django_db


class MockCommonInfo(CommonInfo):
    """The CommonInfo mock class."""

    @staticmethod
    def reset_user() -> None:
        """Reset the request user."""
        d8b.middleware._USER.value = None


def test_common_info_get_current_user(admin: User, admin_client: Client):
    """Should get the current user."""
    MockCommonInfo.reset_user()
    response = admin_client.get(reverse('admin:users_user_changelist'))

    assert response.status_code == 200
    assert CommonInfo.get_current_user() == admin


def test_common_info_set_user_fields_new_user(
    admin: User, admin_client: Client
):
    """Should set user fields for a new user."""
    MockCommonInfo.reset_user()
    commonInfo = MockCommonInfo()
    commonInfo.pk = None
    commonInfo._set_user_fields(admin)

    assert commonInfo.created_by == admin
    assert commonInfo.modified_by == admin


def test_common_info_set_user_fields_existing_user(
    admin: User, admin_client: Client
):
    """Should update user fields for an existing new user."""
    MockCommonInfo.reset_user()
    commonInfo = MockCommonInfo()
    commonInfo.pk = 12
    commonInfo._set_user_fields(admin)

    assert commonInfo.created_by is None
    assert commonInfo.modified_by == admin


def test_common_info_set_user_fields_on_save(
    admin: User, admin_client: Client
):
    """Should set user fields for an user when saving."""
    MockCommonInfo.reset_user()
    response = admin_client.get(reverse('admin:users_user_changelist'))
    commonInfo = MockCommonInfo()
    commonInfo.pk = None
    commonInfo.save()

    assert response.status_code == 200
    assert commonInfo.created_by == admin
    assert commonInfo.modified_by == admin


def test_common_info_set_user_fields_on_save_without_user(
    admin: User, admin_client: Client
):
    """Should skip the setting user fields."""
    MockCommonInfo.reset_user()
    commonInfo = MockCommonInfo()
    commonInfo.pk = None
    commonInfo.save()

    assert commonInfo.created_by is None
    assert commonInfo.modified_by is None
