from django.core import urlresolvers
from django.test import override_settings
from django.test.testcases import TestCase
from mock import patch
from http_adapter.url_types import UrlTypes

urlpatterns = []


class TestUrlReverseCache(TestCase):
    @patch.object(urlresolvers, 'reverse')
    @override_settings(ROOT_URLCONF=__name__)
    def test_url_resolution_cache(self, mocked_reverse):
        mocked_reverse.return_value = '/something/'
        from http_adapter.default_url_generator import CachedUrlReverser
        url_resolver = CachedUrlReverser(
            resource_name='asdf',
            url_type=UrlTypes.detail_url)

        url1 = url_resolver.reverse_to_url()  # first call
        url2 = url_resolver.reverse_to_url()  # second call

        assert url1 == url2 == '/something/'
        assert mocked_reverse.call_count == 1
        assert url_resolver.url_pattern == '/something/'
