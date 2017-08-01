import json
import os
import unittest

from hamcrest.core.assert_that import assert_that
from hamcrest.core.core.isequal import equal_to
from mock import MagicMock

from django_adapter import create_http_handler
from rip.api import Api
from rip.api_schema import ApiSchema
from rip.crud.crud_resource import CrudResource
from rip.generic_steps.default_authentication import DefaultAuthentication
from rip.generic_steps.default_authorization import DefaultAuthorization
from rip.generic_steps.default_entity_actions import DefaultEntityActions
from rip.schema.string_field import StringField


class DummySchema(ApiSchema):
    name = StringField(required=True)

    class Meta:
        schema_name = 'dummy'


class DummyEntityActions(DefaultEntityActions):
    def get_entity_list(self, request, **kwargs):
        return [{
            'name': 'dummy'
        }]

    def get_entity_list_total_count(self, request, **kwargs):
        return 1


class DummyViewAuthorization(DefaultAuthorization):
    pass


class DummyAuthentication(DefaultAuthentication):
    pass


class DummyViewResource(CrudResource):
    schema_cls = DummySchema
    entity_actions_cls = DummyEntityActions
    authorization_cls = DummyViewAuthorization
    authentication_cls = DummyAuthentication


class DummyUser(object):
    def is_anonymous(self):
        return False


class TestApi(unittest.TestCase):
    def setUp(self):
        os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
        self.api = Api(name='api', version='v1')
        self.api.register_resource('dummy', DummyViewResource())
        self.handler = create_http_handler(self.api)

    def test_crud_resource_get_list(self):
        url = 'dummy'
        user = DummyUser()

        http_request = MagicMock(user=user, method='GET')

        response = self.handler(http_request, url)

        assert_that(response.status_code, equal_to(200))
        assert_that(json.loads(response.content), equal_to(
            {"objects": [{"name": "dummy"}], "meta": {"total": 1, "limit": 20, "offset": 0}}))
