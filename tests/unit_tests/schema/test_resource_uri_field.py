import unittest

from hamcrest.core import assert_that
from hamcrest.core.core.isequal import equal_to
from mock import MagicMock

from rip.schema.resource_uri_field import \
    ResourceUriField
from tests import request_factory


class TestResourceUriField(unittest.TestCase):
    def test_should_serialize_resource_uri(self):
        field = ResourceUriField()
        field.schema_cls = schema_cls = MagicMock()
        schema_cls._meta = schema_meta =MagicMock()
        schema_meta.schema_name='test'
        request = request_factory.get_request()

        value = field.serialize(request, 22)

        assert_that(value, equal_to('/api/v2/test/22/'))
