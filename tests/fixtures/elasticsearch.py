"""The elasticsearch fixtures module."""
# pylint: disable=unused-argument, redefined-outer-name

import pytest
from pytest_elasticsearch import factories

from d8b.settings import ENV

params = ENV.str("ELASTICSEARCH_URL").split(":")

elasticsearch_noproc = factories.elasticsearch_noproc(
    port=params[1],
    host=params[0],
)
elasticsearch = factories.elasticsearch("elasticsearch_noproc")


@pytest.fixture()
def elasticsearch_setup(elasticsearch):
    """Set up the elasticsearch."""
