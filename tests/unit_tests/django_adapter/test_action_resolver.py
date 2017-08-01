import unittest

from hamcrest import assert_that, equal_to
from mock import MagicMock

from django_adapter import action_resolver
from django_adapter.crud_resource import CrudResource
from rip.api_schema import ApiSchema
from rip.view.view_resource import ViewResource

__all__ = ["TestActionResolver"]


class MockSchema(ApiSchema):
    class Meta:
        schema_name = 'mock'


class MockResource(CrudResource):
    schema_cls = MockSchema()

class MockViewResource(ViewResource):
    schema_cls = MockSchema()


class TestActionResolver(unittest.TestCase):
    def test_resolve_update_action_on_api(self):
        mock_http_request = MagicMock()
        mock_http_request.method = 'PATCH'
        mock_api = MagicMock()
        mock_resource = MockResource()
        mock_api.resolve_resource.return_value = mock_resource
        mock_resource.update_detail = expected_action = MagicMock()

        action = action_resolver.resolve_action(mock_http_request, api=mock_api,
                                                url='foo/1')
        assert_that(action, equal_to(expected_action))

    def test_resolve_put_action_on_api(self):
        mock_http_request = MagicMock()
        mock_http_request.method = 'PUT'
        mock_api = MagicMock()
        mock_resource = MockResource()
        mock_api.resolve_resource.return_value = mock_resource
        mock_resource.create_or_update_detail = expected_action = MagicMock()

        action = action_resolver.resolve_action(mock_http_request, api=mock_api,
                                                url='foo/1')
        assert_that(action, equal_to(expected_action))

    def test_resolve_detail_action_on_api(self):
        mock_http_request = MagicMock()
        mock_http_request.method = 'DELETE'
        mock_api = MagicMock()
        mock_resource = MockResource()
        mock_api.resolve_resource.return_value = mock_resource
        mock_resource.delete_detail = expected_delete_action = MagicMock()

        action = action_resolver.resolve_action(mock_http_request, api=mock_api,
                                                url='foo/1')
        assert_that(action, equal_to(expected_delete_action))

    def test_resolve_post_on_list_as_create_detail(self):
        mock_http_request = MagicMock()
        mock_http_request.method = 'POST'
        mock_api = MagicMock()
        mock_resource = MockResource()
        mock_api.resolve_resource.return_value = mock_resource
        mock_resource.create_detail = expected_create_action = MagicMock()

        action = action_resolver.resolve_action(mock_http_request, api=mock_api,
                                                url='foo')
        assert_that(action, equal_to(expected_create_action))

    def test_resolve_non_existing_endpoint(self):
        mock_http_request = MagicMock()
        mock_http_request.method = 'DELETE'
        mock_api = MagicMock(
            spec_set=[])

        action = action_resolver.resolve_action(mock_http_request, api=mock_api,
                                                url='foo')
        assert_that(action, equal_to(None))

    def test_resolve_non_existing_action_delete(self):
        mock_http_request = MagicMock()
        mock_http_request.method = 'DELETE'
        mock_api = MagicMock()
        mock_resource = object()
        mock_api.resolve_resource.return_value = mock_resource

        action = action_resolver.resolve_action(mock_http_request, api=mock_api,
                                                url='foo')
        assert_that(action, equal_to(None))

    def test_resolve_non_existing_action_put(self):
        mock_http_request = MagicMock()
        mock_http_request.method = 'PUT'
        mock_api = MagicMock()
        mock_resource = object()
        mock_api.resolve_resource.return_value = mock_resource

        action = action_resolver.resolve_action(mock_http_request, api=mock_api,
                                                url='foo')
        assert_that(action, equal_to(None))

    def test_resolve_non_existing_action_options(self):
        mock_http_request = MagicMock()
        mock_http_request.method = 'OPTIONS'
        mock_api = MagicMock()
        mock_resource = object()
        mock_api.resolve_resource.return_value = mock_resource

        action = action_resolver.resolve_action(mock_http_request, api=mock_api,
                                                url='foo')
        assert_that(action, equal_to(None))

    def test_resolve_view_action(self):
        mock_http_request = MagicMock()
        mock_http_request.method = 'GET'
        mock_api = MagicMock()
        mock_resource = MockViewResource()
        mock_api.resolve_resource.return_value = mock_resource
        mock_resource.read = expected_read_action = MagicMock()

        action = action_resolver.resolve_action(mock_http_request, api=mock_api,
                                                url='foo')
        assert_that(action, equal_to(expected_read_action))
