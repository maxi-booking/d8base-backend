"""The services tests module."""
from dataclasses import dataclass

from d8b.services import RandomFilenameGenerator


def test_random_filename_generator():
    """Should generate a random filename."""

    @dataclass
    class MockInstance():
        """The mock instance."""

        test_field: str

    generator = RandomFilenameGenerator('test_path', 'test')

    assert 'test_path/_/' in generator(MockInstance('test id'), 'test.jpg')

    generator = RandomFilenameGenerator('test_path', 'test_field')

    assert 'test_path/test-id/' in generator(
        MockInstance('test-id'),
        'test.jpg',
    )
    path1 = generator(MockInstance('test id'), 'test.jpg')
    path2 = generator(MockInstance('test id'), 'test.jpg')

    assert path1 != path2
