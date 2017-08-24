import json
import unittest
from mock import MagicMock

from http_adapter.django_crud_resource import DjangoResource
from http_adapter.url_types import UrlTypes
from rip.generic_steps.default_entity_actions import DefaultEntityActions
from rip.schema_fields.string_field import StringField
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'


class DummyEntityActions(DefaultEntityActions):
    def get_entity_list(self, request, **kwargs):
        return [{
            'name': 'dummy'
        }]

    def get_entity_list_total_count(self, request, **kwargs):
        return 1


class DummyViewResource(DjangoResource):
    name = StringField(required=True)

    class Meta:
        entity_actions_cls = DummyEntityActions


class DummyUser(object):
    def is_anonymous(self):
        return False


class TestApi(unittest.TestCase):

    def test_crud_resource_get_list(self):
        url = 'dummy'
        user = DummyUser()

        http_request = MagicMock(user=user, method='GET')

        response = DummyViewResource.as_view()(
            http_request, url_type=UrlTypes.list_url)

        assert response.status_code == 200
        assert json.loads(response.content) == \
            {"objects": [{"name": "dummy"}],
             "meta": {"total": 1, "limit": 20, "offset": 0}}
