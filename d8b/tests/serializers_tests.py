"""The d8b serializers tests module."""
import pytest
from django.contrib.auth import get_user_model
from pytest_mock import MockFixture

from d8b.serializers import ModelCleanFieldsSerializer
from users.models import User

pytestmark = pytest.mark.django_db


class MockModelCleanFieldsSerializer(ModelCleanFieldsSerializer):
    """The mock ModelCleanFieldsSerializer."""

    class Meta():
        """The metainfomation class."""

        model = get_user_model()


def test_model_clean_fields_serializer(mocker: MockFixture):
    """Should call the model clean method."""
    full_clean = mocker.Mock(return_value="full_clean")
    clean = mocker.Mock(return_value="clean")
    serializer = MockModelCleanFieldsSerializer()
    serializer.Meta.model.full_clean = full_clean
    serializer.validate({})

    assert full_clean.called

    copy_mock = mocker.patch("d8b.serializers.deepcopy")
    copy_mock.return_value = clean
    serializer.instance = User()
    serializer.instance.clean = clean
    serializer.validate({})

    copy_mock.assert_called_once_with(serializer.instance)
    clean.clean.assert_called_once()
