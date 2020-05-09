"""The d8b serializers tests module."""
import pytest
from django.contrib.auth import get_user_model
from pytest_mock.plugin import MockFixture

from d8b.serializers import ModelCleanFieldsSerializer

pytestmark = pytest.mark.django_db


class MockModelCleanFieldsSerializer(ModelCleanFieldsSerializer):
    """The mock ModelCleanFieldsSerializer."""

    class Meta():
        """The metainfomation class."""

        model = get_user_model()


def test_model_clean_fields_serializer(mocker: MockFixture):
    """Should call the model clean method."""
    clean = mocker.Mock(return_value='clean')
    serializer = MockModelCleanFieldsSerializer()
    serializer.Meta.model.clean = clean
    serializer.validate({})

    assert clean.called
