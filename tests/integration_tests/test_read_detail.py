import json

from django.conf.urls import url, include
from django.core import urlresolvers
from django.test import override_settings

from tests.integration_tests.base_test_case import \
    EndToEndBaseTestCase
from tests.integration_tests.resources_for_testing import PersonEntity, router, PersonDataManager

urlpatterns = [
    url(r'^hello/', include(router.urls)),
]


@override_settings(ROOT_URLCONF=__name__)
class GetCrudResourceIntegrationTest(EndToEndBaseTestCase):
    def test_should_get_fields(self):
        expected_entities = [PersonEntity(name='John', email=None, phone='1234',
                                          id='John',
                                          address={'city': 'bangalore',
                                                   'country': 'India'},
                                          company=None,
                                          nick_names=['Johnny', 'Papa'])]
        PersonDataManager.get_entity_list.return_value = expected_entities

        response = self.client.get(urlresolvers.reverse(
            'person-detail', args=('John',)))

        assert response.status_code == 200
        assert json.loads(response.content) == expected_entities[0].__dict__

    def test_should_get_by_allowed_filters(self):
        expected_entities = [PersonEntity(name='John', email=None, phone='1234',
                                          address={'city': 'bangalore',
                                                   'country': 'India'},
                                          company=None,
                                          nick_names=['Johnny', 'Papa'])]

        PersonDataManager.get_entity_list.return_value = expected_entities

        response = self.client.get(urlresolvers.reverse(
            'person-detail', args=('John',)), data={'name': 'bar'})

        assert response.status_code == 200
        assert PersonDataManager.get_entity_list.call_count == 1
        call_kwargs = PersonDataManager.get_entity_list.call_args[1]
        assert call_kwargs['name'] == 'bar'
        assert call_kwargs['id'] == 'John'

    def test_should_get_none_for_nullable_schema_field(self):
        expected_entities = [PersonEntity(name='John', email=None,
                                          phone='1234',
                                          address=None, company=None,
                                          nick_names=['Johnny', 'Papa'])]
        PersonDataManager.get_entity_list.return_value = expected_entities

        response = self.client.get(urlresolvers.reverse(
            'person-detail', args=('John',)))

        assert response.status_code == 200
        expected_data = expected_entities[0].__dict__
        assert json.loads(response.content) == expected_data

    def test_should_serialize_company(self):
        expected_entities = [PersonEntity(name='John', email=None,
                                          phone='1234',
                                          address=None, company='asdf',
                                          nick_names=['Johnny', 'Papa'])]
        PersonDataManager.get_entity_list.return_value = expected_entities

        response = self.client.get(urlresolvers.reverse(
            'person-detail', args=('John',)))

        assert response.status_code == 200
        expected_data = expected_entities[0].__dict__
        expected_data['company'] = '/hello/company/asdf/'
        assert json.loads(response.content) == expected_data

    def test_should_error_for_non_nullable_fields(self):
        expected_entities = [PersonEntity(name=None, email=None,
                                          phone='1234',
                                          address=None, company='asdf',
                                          nick_names=['Johnny', 'Papa'])]
        PersonDataManager.get_entity_list.return_value = expected_entities

        response = self.client.get(urlresolvers.reverse(
            'person-detail', args=('John',)))

        assert response.status_code == 200
