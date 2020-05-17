"""The pytest fixtures module."""
# pylint: disable=invalid-name
collect_ignore_glob = ['*/migrations/*']

pytest_plugins = [
    'tests.fixtures.auth',
    'tests.fixtures.locations',
    'tests.fixtures.users',
    'tests.fixtures.professionals',
    'tests.fixtures.communication',
]

ADMIN_EMAIL = 'admin@example.com'
ADMIN_PASSWORD = 'admin_password'
USER_EMAIL = 'user@example.com'
USER_PASSWORD = 'user_password'
OBJECTS_TO_CREATE = 5
