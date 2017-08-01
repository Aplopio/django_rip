import json
import os
import unittest

from hamcrest.core.assert_that import assert_that
from hamcrest.core.core.isequal import equal_to
from mock import MagicMock

from django_adapter import create_http_handler
from django_adapter.api import Api
from django_adapter.view.view_resource import ViewResource
from rip.generic_steps.default_authentication import DefaultAuthentication
from rip.generic_steps.default_view_actions import DefaultViewActions
from rip.generic_steps.default_view_authorization import DefaultViewAuthorization
from rip.schema.api_schema import ApiSchema
from rip.schema.string_field import StringField


class DummySchema(ApiSchema):
    name = StringField(required=True)

    class Meta:
        schema_name = 'dummy'


class DummyViewActions(DefaultViewActions):
    def view(self, request):
        return {
            'name': 'dummy'
        }


class DummyViewAuthorization(DefaultViewAuthorization):
    pass


class DummyAuthentication(DefaultAuthentication):
    pass


class DummyViewResource(ViewResource):
    schema_cls = DummySchema
    view_actions_cls = DummyViewActions
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

    def test_view_resource(self):
        url = 'dummy'
        user = DummyUser()

        http_request = MagicMock(user=user, method='GET')

        response = self.handler(http_request, url)

        assert_that(response.status_code, equal_to(200))
        assert_that(json.loads(response.content), equal_to({'name': 'dummy'}))
