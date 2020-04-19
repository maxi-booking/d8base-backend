"""The tasks tests module."""
from djmoney import settings
from pytest_mock.plugin import MockFixture

from d8b.tasks import update_rates


def test_update_rates(mocker: MockFixture):
    """Should update the currency rates."""
    mock = mocker.patch(settings.EXCHANGE_BACKEND)
    update_rates()
    assert mock.call_count == 1
