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
class PutCrudResourceIntegrationTest(EndToEndBaseTestCase):
    def test_should_update_fields(self):
        expected_entity = PersonEntity(name='John', email="foo@bar.com",
                                       phone='1234',
                                       address={'city': 'bangalore',
                                                'country': 'India'},
                                       company=None,
                                       nick_names=['Johnny', 'Papa'])
        PersonDataManager.get_entity_list.return_value = [expected_entity]
        PersonDataManager.update_entity.return_value = expected_entity
        PersonDataManager.get_entity_list_total_count.return_value = 1

        response = self.client.put(
            urlresolvers.reverse('person-detail', args=('John',)),
            data=json.dumps(expected_entity.__dict__),
            content_type="application/json")

        assert response.status_code == 200
        expected_data = expected_entity.__dict__
        assert json.loads(response.content) == expected_data

        expected_update_kwargs = expected_data.copy()
        expected_update_kwargs.pop('phone')
        expected_update_kwargs['address'].pop('city')
        # assert readonly fields are ignored when calling update
        call_args = PersonDataManager.update_entity.call_args[1]
        assert call_args == expected_update_kwargs

    def test_success_when_nullable_fields_set_to_none(self):
        expected_entity = PersonEntity(
            name='John', email=None, phone='1234', address=None, company=None,
            nick_names=['Johnny', 'Papa'])

        PersonDataManager.get_entity_list.return_value = [expected_entity]
        PersonDataManager.update_entity.return_value = expected_entity
        PersonDataManager.get_entity_list_total_count.return_value = 1

        response = self.client.put(
            urlresolvers.reverse('person-detail', args=('John',)),
            data=json.dumps(expected_entity.__dict__),
            content_type="application/json")

        assert response.status_code == 200
        call_args = PersonDataManager.update_entity.call_args[1]
        assert call_args['email'] is None

    def test_failure_when_required_fields_are_not_present(self):
        expected_entity = PersonEntity(email=None,
                                       phone='1234',
                                       address=None, company=None,
                                       nick_names=['Johnny', 'Papa'])
        PersonDataManager.get_entity_list.return_value = [expected_entity]
        PersonDataManager.update_entity.return_value = expected_entity
        PersonDataManager.get_entity_list_total_count.return_value = 1

        response = self.client.put(
            urlresolvers.reverse('person-detail', args=('John',)),
            data=json.dumps(expected_entity.__dict__),
            content_type="application/json")

        assert response.status_code == 400
        assert 'name' in json.loads(response.content)

    def test_update_when_non_nullable_fields_are_set_to_none(self):
        expected_entity = PersonEntity(name=None, email=None,
                                       phone='1234',
                                       address=None, company=None)

        PersonDataManager.get_entity_list.return_value = [expected_entity]
        PersonDataManager.update_entity.return_value = expected_entity
        PersonDataManager.get_entity_list_total_count.return_value = 1

        response = self.client.put(
            urlresolvers.reverse('person-detail', args=('John',)),
            data=json.dumps(expected_entity.__dict__),
            content_type="application/json")

        assert response.status_code == 400
        assert 'name' in json.loads(response.content)
