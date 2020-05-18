"""The logging tests module."""

from pytest_mock.plugin import MockFixture

from d8b.logging import log


def test_log_decorator(mocker: MockFixture):
    """Should log the function."""
    patcher = mocker.patch('logging.getLogger')

    @log('test message')
    def test_function(one, two):
        """Run the test function."""
        return one, two

    test_function('one', 2)
    assert patcher.called
    assert patcher.call_count == 1
    assert str(patcher.call_args) == "call('d8b')"
