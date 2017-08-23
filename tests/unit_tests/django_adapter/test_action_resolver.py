import unittest
from mock import MagicMock

from http_adapter.default_rip_action_resolver import DefaultRipActionResolver
from http_adapter.url_types import UrlTypes
from rip.crud.crud_actions import CrudActions

__all__ = ["TestDefaultRipActionResolver"]


class TestEndPoint(unittest.TestCase):
    def test_any_request_with_id_eq_detail(self):
        for method in ['PATCH', 'PUT', 'DELETE', 'GET', 'POST']:
            mock_http_request = MagicMock()
            mock_http_request.method = method
            url_kwargs = {'id': 1}

            action_resolver = DefaultRipActionResolver(
                http_request=mock_http_request, url_type=UrlTypes.detail_url,
                url_kwargs=url_kwargs)

            assert action_resolver.determine_end_point() == 'detail'

    def test_request_with_on_list_eq_none(self):
        mock_http_request = MagicMock()
        mock_http_request.method = 'GET'
        url_kwargs = {'id': 1}

        action_resolver = DefaultRipActionResolver(
            http_request=mock_http_request, url_type=UrlTypes.list_url,
            url_kwargs=url_kwargs)

        assert action_resolver.determine_end_point() == 'list'

    def test_post_on_list_eq_detail(self):
        mock_http_request = MagicMock()
        mock_http_request.method = 'POST'
        url_kwargs = {'sdaf': 1}

        action_resolver = DefaultRipActionResolver(
            http_request=mock_http_request, url_type=UrlTypes.list_url,
            url_kwargs=url_kwargs)

        assert action_resolver.determine_end_point() == 'detail'

    def test_get_on_list_eq_list(self):
        mock_http_request = MagicMock()
        mock_http_request.method = 'GET'
        url_kwargs = {'sdaf': 1}

        action_resolver = DefaultRipActionResolver(
            http_request=mock_http_request, url_type=UrlTypes.list_url,
            url_kwargs=url_kwargs)

        assert action_resolver.determine_end_point() == 'list'

    def test_unallowed_actions_on_list_ret_none(self):
        for method in ['PATCH', 'PUT', 'DELETE']:
            mock_http_request = MagicMock()
            mock_http_request.method = method
            url_kwargs = {}

            action_resolver = DefaultRipActionResolver(
                http_request=mock_http_request, url_type=UrlTypes.list_url,
                url_kwargs=url_kwargs)

            assert action_resolver.determine_end_point() is None


class TestActionName(unittest.TestCase):

    def test_aggregates_on_get(self):
        mock_http_request = MagicMock()
        mock_http_request.method = "GET"

        action_resolver = DefaultRipActionResolver(
            http_request=mock_http_request, url_type=UrlTypes.aggregates_url,
            url_kwargs={})

        assert action_resolver.get_action_name() == CrudActions.GET_AGGREGATES

    def test_aggregates_on_post(self):
        mock_http_request = MagicMock()
        mock_http_request.method = "POST"

        action_resolver = DefaultRipActionResolver(
            http_request=mock_http_request, url_type=UrlTypes.aggregates_url,
            url_kwargs={})

        assert action_resolver.get_action_name() is None

    def test_create_action(self):
        mock_http_request = MagicMock()
        mock_http_request.method = "POST"

        action_resolver = DefaultRipActionResolver(
            http_request=mock_http_request, url_type=UrlTypes.list_url,
            url_kwargs={})

        assert action_resolver.get_action_name() == CrudActions.CREATE_DETAIL

    def test_patch_request_on_detail(self):
        mock_http_request = MagicMock()
        mock_http_request.method = "PATCH"

        action_resolver = DefaultRipActionResolver(
            http_request=mock_http_request, url_type=UrlTypes.detail_url,
            url_kwargs={'id': 1})

        assert action_resolver.get_action_name() == CrudActions.UPDATE_DETAIL

    def test_patch_request_on_list(self):
        mock_http_request = MagicMock()
        mock_http_request.method = "PATCH"

        action_resolver = DefaultRipActionResolver(
            http_request=mock_http_request, url_type=UrlTypes.list_url,
            url_kwargs={'id': 1})
        assert action_resolver.get_action_name() is None
