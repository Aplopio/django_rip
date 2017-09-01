import json

from django.conf.urls import url, include
from django.core import urlresolvers
from django.test import override_settings

from tests.integration_tests.base_test_case import \
    EndToEndBaseTestCase
from tests.integration_tests.resources_for_testing import \
    PersonEntity, PersonDataManager, router

urlpatterns = [
    url(r'^hello/', include(router.urls)),
]


@override_settings(ROOT_URLCONF=__name__)
class ListCrudResourceIntegrationTest(EndToEndBaseTestCase):

    def test_should_get_list(self):
        expected_entities = [
            PersonEntity(name='John', email=None, phone='1234',
                         address={'city': 'bangalore', 'country': 'India'},
                         nick_names=['Johnny', 'Papa'])]
        PersonDataManager.get_entity_list.return_value = expected_entities
        PersonDataManager.get_entity_list_total_count.return_value = 1

        response = self.client.get(urlresolvers.reverse('person-list'))

        assert response.status_code == 200
        expected_entity = expected_entities[0].__dict__.copy()
        expected_data = [expected_entity]
        response_data = json.loads(response.content)
        assert response_data['objects'] == expected_data
        assert response_data['meta']['total'] == 1

    def test_should_get_list_fields_only(self):
        expected_entities = [
            PersonEntity(name='John', email=None, phone='1234',
                         address={'city': 'bangalore', 'country': 'India'},
                         nick_names=['Johnny', 'Papa'], company=None)]
        PersonDataManager.get_entity_list.return_value = expected_entities
        PersonDataManager.get_entity_list_total_count.return_value = 1

        response = self.client.get(urlresolvers.reverse('person-list'))

        assert response.status_code == 200

        response_entity = json.loads(response.content)['objects'][0]
        self.assertTrue('company' not in response_entity)

    def test_should_fail_ordering_for_unallowed_field_ordering(self):
        expected_entities = [PersonEntity(
            name='John', email=None, phone='1234',
            address={'city': 'bangalore', 'country': 'India'}, company=None)]
        PersonDataManager.get_entity_list.return_value = expected_entities
        PersonDataManager.get_entity_list_total_count.return_value = 1

        response = self.client.get(urlresolvers.reverse('person-list'),
                                   data={'order_by': 'email'})

        assert response.status_code == 400
        response_content = json.loads(response.content)
        assert ('email', 'Ordering not allowed') in response_content.items()

    def test_should_order_by_allowed_field(self):
        expected_entities = [PersonEntity(
            name='John', email=None, phone='1234',
            address={'city': 'bangalore', 'country': 'India'},
            company=None, nick_names=['Johnny', 'Papa'])]

        PersonDataManager.get_entity_list.return_value = expected_entities
        PersonDataManager.get_entity_list_total_count.return_value = 1

        response = self.client.get(urlresolvers.reverse('person-list'),
                                   data={'order_by': 'name'})

        assert response.status_code == 200

    def test_should_filter_by_list_field(self):
        expected_entities = [PersonEntity(name='John', email=None, phone='1234',
                                          address={'city': 'bangalore',
                                                   'country': 'India'},
                                          company=None,
                                          nick_names=['Johnny', 'Papa'])]
        PersonDataManager.get_entity_list.return_value = expected_entities
        PersonDataManager.get_entity_list_total_count.return_value = 1

        response = self.client.get(urlresolvers.reverse('person-list'),
                                   data={'nick_names': 'Johnny'})

        assert response.status_code == 200
        assert 'Johnny' in json.loads(response.content)['objects'][0]['nick_names']
        call_args = PersonDataManager.get_entity_list.call_args[1]
        assert call_args['nick_names'] == ['Johnny']

    def test_should_filter_by_in(self):
        expected_entities = [PersonEntity(
            name='John', email=None, phone='1234',
            address={'city': 'bangalore', 'country': 'India'},
            company=None, nick_names=['Johnny', 'Papa'])]

        PersonDataManager.get_entity_list.return_value = expected_entities
        PersonDataManager.get_entity_list_total_count.return_value = 1

        response = self.client.get(
            urlresolvers.reverse('person-list'),
            data={'nick_names__in': ['somename', 'someothername']})

        assert response.status_code == 200
        call_args = PersonDataManager.get_entity_list.call_args[1]
        assert call_args['nick_names__in'] == ['somename', 'someothername']

    def test_should_filter_by_gt(self):
        expected_entities = [PersonEntity(
            name='John', email=None, phone='1234',
            address={'city': 'bangalore', 'country': 'India'},
            company=None, nick_names=['Johnny', 'Papa'])]

        PersonDataManager.get_entity_list.return_value = expected_entities
        PersonDataManager.get_entity_list_total_count.return_value = 1

        response = self.client.get(
            urlresolvers.reverse('person-list'),
            data={'name__gt': 'somename'})

        assert response.status_code == 200
        call_args = PersonDataManager.get_entity_list.call_args[1]
        assert call_args['name__gt'] == 'somename'
