from mock import patch
from django.conf.urls import url, include
from django.core import urlresolvers
from django.test import TestCase
from django.test import override_settings

from http_adapter.default_url_generator import DefaultUrlReverser, \
    CachedUrlReverser
from http_adapter.django_crud_resource import DjangoResource
from http_adapter.django_router import DefaultRouter
from http_adapter.url_types import UrlTypes
from rip.crud import crud_actions
from rip.schema_fields.integer_field import IntegerField


class TestResource(DjangoResource):
    id = IntegerField(nullable=False)

    class Meta:
        resource_name = 'test'
        allowed_actions = crud_actions.ALL_ACTIONS


class ComplexResource(TestResource):
    class Meta:
        resource_name = 'complex'


router = DefaultRouter()
router.register(TestResource)
router.register(ComplexResource, 'test/{test_id}/complex')

urlpatterns = [
    url(r'^hello/', include(router.urls)),
]


@override_settings(ROOT_URLCONF=__name__)
class TestUrlReverser(TestCase):

    def test_detail_revers(self):
        url_resolver = DefaultUrlReverser(
            resource_name=TestResource.get_meta().resource_name,
            url_type='detail')
        assert url_resolver.reverse_to_url(value=2) == '/hello/test/2/'

    def test_url_list_reverse(self):
        url_resolver = DefaultUrlReverser(
            resource_name=TestResource.get_meta().resource_name,
            url_type='list')
        assert url_resolver.reverse_to_url() == '/hello/test/'

    def test_url_aggregates_reverse(self):
        url_resolver = DefaultUrlReverser(
            resource_name=TestResource.get_meta().resource_name,
            url_type=UrlTypes.aggregates_url)
        assert url_resolver.reverse_to_url() == '/hello/test/aggregates/'

    def test_complex_detail_reverse(self):
        url_resolver = DefaultUrlReverser(
            resource_name=ComplexResource.get_meta().resource_name,
            url_type='detail')
        assert url_resolver.reverse_to_url([2, 1]) == '/hello/test/2/complex/1/'

    def test_complex_list_reverse(self):
        url_resolver = DefaultUrlReverser(
            resource_name=ComplexResource.get_meta().resource_name,
            url_type='list')
        assert url_resolver.reverse_to_url([2]) == '/hello/test/2/complex/'

    def test_complex_aggregate_reverse(self):
        url_resolver = DefaultUrlReverser(
            resource_name=ComplexResource.get_meta().resource_name,
            url_type=UrlTypes.aggregates_url)
        assert url_resolver.reverse_to_url([2]) == \
               '/hello/test/2/complex/aggregates/'

@override_settings(ROOT_URLCONF=__name__)
class TestCachedUrlResolver(TestCase):
    def setUp(self):
        pass

    def test_url_detail_reverse(self):
        url_resolver = CachedUrlReverser(
            resource_name=TestResource.get_meta().resource_name,
            url_type='detail')
        assert url_resolver.reverse_to_url(value=2) == '/hello/test/2/'

    def test_url_list_reverse(self):
        url_resolver = CachedUrlReverser(
            resource_name=TestResource.get_meta().resource_name,
            url_type='list')
        assert url_resolver.reverse_to_url() == '/hello/test/'

    def test_url_aggregates_reverse(self):
        url_resolver = CachedUrlReverser(
            resource_name=TestResource.get_meta().resource_name,
            url_type=UrlTypes.aggregates_url)
        assert url_resolver.reverse_to_url() == '/hello/test/aggregates/'

