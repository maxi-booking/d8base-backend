"""The models tests module."""
import pytest
from django.db import connection
from django.db.utils import ProgrammingError
from django.test.client import Client
from django.urls import reverse
from pytest_mock import MockFixture

import d8b.middleware
from d8b.models import CommonInfo, ValidationMixin
from users.models import User

pytestmark = pytest.mark.django_db

# pylint: disable=redefined-outer-name, protected-access


@pytest.fixture(scope="module")
def mock_common_info_class(django_db_blocker):
    """Get the mock of the CommomInfo class."""

    class MockCommonInfo(CommonInfo, ValidationMixin):
        """The CommonInfo mock class."""

        @staticmethod
        def reset_user() -> None:
            """Reset the request user."""
            d8b.middleware._USER.value = None

    with django_db_blocker.unblock():
        try:
            with connection.schema_editor() as schema_editor:
                schema_editor.create_model(MockCommonInfo)
        except ProgrammingError:
            pass
    return MockCommonInfo


@pytest.fixture(scope="function")
def mock_common_info(mock_common_info_class):
    """Get the instance of mock of the CommomInfo class."""
    return mock_common_info_class()


def test_common_info_get_current_user(
    admin: User,
    admin_client: Client,
    mock_common_info,
):
    """Should get the current user."""
    mock_common_info.reset_user()
    response = admin_client.get(reverse("admin:users_user_changelist"))

    assert response.status_code == 200
    assert CommonInfo.get_current_user() == admin


def test_common_info_set_user_fields_new_user(
    admin: User,
    mock_common_info,
):
    """Should set user fields for a new user."""
    mock_common_info.reset_user()
    mock_common_info.pk = None
    mock_common_info._set_user_fields(admin)

    assert mock_common_info.created_by == admin
    assert mock_common_info.modified_by == admin


def test_common_info_set_user_fields_existing_user(
    admin: User,
    mock_common_info,
):
    """Should update user fields for an existing new user."""
    mock_common_info.reset_user()
    mock_common_info.pk = 12
    mock_common_info._set_user_fields(admin)

    assert mock_common_info.created_by is None
    assert mock_common_info.modified_by == admin


def test_common_info_set_user_fields_on_save(
    admin: User,
    admin_client: Client,
    mock_common_info,
):
    """Should set user fields for a user when saving."""
    mock_common_info.reset_user()
    response = admin_client.get(reverse("admin:users_user_changelist"))
    mock_common_info.pk = None
    mock_common_info.save()

    assert response.status_code == 200
    assert mock_common_info.created_by == admin
    assert mock_common_info.modified_by == admin


def test_common_info_set_user_fields_on_save_without_user(mock_common_info):
    """Should skip the setting user fields."""
    mock_common_info.reset_user()
    mock_common_info.pk = None
    mock_common_info.save()

    assert mock_common_info.created_by is None
    assert mock_common_info.modified_by is None


def test_validation_mixin(mock_common_info, mocker: MockFixture):
    """Should run validators."""
    validator1 = mocker.Mock(return_value="validator1")
    validator2 = mocker.Mock(return_value="validator2")
    mock_common_info.validators = [validator1, validator2]
    mock_common_info.clean()

    assert validator1.called
    assert validator2.called
