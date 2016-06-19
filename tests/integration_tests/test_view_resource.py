import unittest

from hamcrest.core import assert_that
from hamcrest.core.core.isequal import equal_to
from mock import patch

from rip import error_types
from rip.api_schema import ApiSchema
from rip.default_view_actions import DefaultViewActions
from rip.generic_steps.default_authentication import DefaultAuthentication
from rip.response import Response
from rip.schema.string_field import StringField
from rip.view.default_view_authorization import DefaultViewAuthorization
from rip.view.view_resource import ViewResource
from tests import request_factory
from tests.utils import patch_class_field


class DummySchema(ApiSchema):
    name = StringField(required=True)


class DummyViewActions(DefaultViewActions):
    def view(self, request):
        return {
            'name': 'dummy'
        }


class DummyAuthorization(DefaultViewAuthorization):
    pass


class DummyAuthentication(DefaultAuthentication):
    pass


class DummyResource(ViewResource):
    schema_cls = DummySchema
    view_actions_cls = DummyViewActions
    authorization_cls = DummyAuthorization
    authentication_cls = DummyAuthentication


class TestViewResource(unittest.TestCase):
    def test_view_returns_value(self):
        resource = DummyResource()

        response = resource.read(request_factory.get_request(user=object()))

        assert_that(response.data, equal_to({'name': 'dummy'}))

    @patch.object(DummyViewActions, 'view')
    def test_when_view_returns_bad_schema(self, mocked_view):
        mocked_view.return_value = {'foo': 'bar'}

        resource = DummyResource()

        with(self.assertRaises(AttributeError)):
            resource.read(request_factory.get_request(user=object()))

    @patch.object(DummyAuthorization, 'authorize_read')
    def test_when_authorization_fails(self, mocked_authorize_read):
        mocked_authorize_read.return_value = Response(is_success=False,
                                                      reason=error_types.ActionForbidden,
                                                      data={'foo': 'bar'})

        response = DummyResource().read(request=request_factory.get_request(user=object()))

        assert_that(response.is_success, equal_to(False))
        assert_that(response.reason, equal_to(error_types.ActionForbidden))
        assert_that(response.data, equal_to({'foo': 'bar'}))

    @patch.object(DummyAuthentication, 'authenticate')
    def test_when_authentication_fails(self, mocked_authenticate):
        mocked_authenticate.return_value = Response(is_success=False,
                                                    reason=error_types.AuthenticationFailed,
                                                    data={'foo': 'bar'})

        response = DummyResource().read(request=request_factory.get_request(user=object()))

        assert_that(response.is_success, equal_to(False))
        assert_that(response.reason, equal_to(error_types.AuthenticationFailed))
        assert_that(response.data, equal_to({'foo': 'bar'}))

    @patch_class_field(DummyResource, 'allowed_actions', [])
    def test_when_method_not_allowed(self):
        response = DummyResource().read(request=request_factory.get_request(user=object()))

        assert_that(response.is_success, equal_to(False))
        assert_that(response.reason, equal_to(error_types.MethodNotAllowed))

