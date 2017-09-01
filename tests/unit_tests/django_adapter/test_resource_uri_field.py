import unittest

from mock import MagicMock

from http_adapter.url_fields import ResourceUriField
from tests import request_factory


class TestResourceUriField(unittest.TestCase):
    def test_should_serialize_resource_uri(self):
        UrlReverser = MagicMock()
        UrlReverser.return_value = url_reverser = MagicMock()
        url_reverser.reverse_to_url = reverse_to_url = MagicMock()

        field = ResourceUriField(resource_name='dfg', entity_attribute='asdf',
                                 url_type='asdf', url_reverser_cls=UrlReverser)
        field.schema_cls = schema_cls = MagicMock()
        request = request_factory.get_request()

        field.serialize(request, 22)

        reverse_to_url.assert_called_once_with(22)
