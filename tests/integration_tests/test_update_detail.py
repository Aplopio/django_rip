from rip.crud.crud_actions import CrudActions
from rip.generic_steps import error_types
from tests import request_factory
from tests.integration_tests.person_base_test_case import \
    PersonResourceBaseTestCase
from tests.integration_tests.resources_for_testing import PersonResource, PersonEntity
import json

from django.conf.urls import url, include
from django.core import urlresolvers
from django.test import override_settings

from tests.integration_tests.person_base_test_case import \
    PersonResourceBaseTestCase
from tests.integration_tests.resources_for_testing import \
    PersonEntity, PersonDataManager, router

urlpatterns = [
    url(r'^hello/', include(router.urls)),
]


@override_settings(ROOT_URLCONF=__name__)
class UpdateCrudResourceIntegrationTest(PersonResourceBaseTestCase):
    def test_should_update_fields(self):
        expected_entity = PersonEntity(name='John', email="foo@bar.com",
                                       phone='1234',
                                       address={'city': 'bangalore',
                                                'country': 'India'},
                                       company=None,
                                       nick_names=['Johnny', 'Papa'])

        PersonDataManager.get_entity_list.return_value = [expected_entity]
        PersonDataManager.update_entity.return_value = expected_entity

        response = self.client.patch(
            urlresolvers.reverse('person-detail', args=('John',)),
            data=json.dumps(expected_entity.__dict__),
            content_type="application/json")

        assert response.status_code == 202

        expected_data = expected_entity.__dict__
        assert json.loads(response.content) == expected_data

        expected_update_kwargs = expected_data.copy()
        expected_update_kwargs.pop('phone')
        expected_update_kwargs['address'].pop('city')

        call_args = PersonDataManager.update_entity.call_args[1]
        assert call_args == expected_update_kwargs

    def test_success_when_nullable_fields_set_to_none(self):
        expected_entity = PersonEntity(name='John', email=None,
                                       phone='1234',
                                       address=None, company=None,
                                       nick_names=['Johnny', 'Papa'])

        PersonDataManager.get_entity_list.return_value = [expected_entity]
        PersonDataManager.update_entity.return_value = expected_entity

        response = self.client.patch(
            urlresolvers.reverse('person-detail', args=('John',)),
            data=json.dumps(expected_entity.__dict__),
            content_type="application/json")

        assert response.status_code == 202
        assert json.loads(response.content) == expected_entity.__dict__
        call_args = PersonDataManager.update_entity.call_args[1]
        assert call_args['email'] is None

    def test_success_when_one_required_fields_are_not_present(self):
        expected_entity = PersonEntity(email=None,
                                       name="john",
                                       address=None, company=None,
                                       nick_names=['Johnny', 'Papa'])
        PersonDataManager.get_entity_list.return_value = [expected_entity]
        PersonDataManager.update_entity.return_value = expected_entity

        post_data = expected_entity.__dict__.copy()
        post_data.pop('name')
        response = self.client.patch(
            urlresolvers.reverse('person-detail', args=('John',)),
            data=json.dumps(post_data),
            content_type="application/json")

        assert response.status_code == 202
        call_args = PersonDataManager.update_entity.call_args[1]
        assert 'name' not in call_args
        assert post_data == call_args

    def test_readonly_fields_are_ignored(self):
        expected_entity = PersonEntity(email=None,
                                       name='John',
                                       phone='1212',
                                       address=None, company=None,
                                       nick_names=['Johnny', 'Papa'])
        PersonDataManager.get_entity_list.return_value = [expected_entity]
        PersonDataManager.update_entity.return_value = expected_entity

        response = self.client.patch(
            urlresolvers.reverse('person-detail', args=('John',)),
            data=json.dumps(expected_entity.__dict__),
            content_type="application/json")

        assert response.status_code == 202
        call_args = PersonDataManager.update_entity.call_args[1]
        assert 'phone' not in call_args

    def test_update_when_non_nullable_fields_are_set_to_none(self):
        expected_entity = PersonEntity(name=None, email=None,
                                       phone='1234',
                                       address=None, company=None)
        PersonDataManager.get_entity_list.return_value = [expected_entity]
        PersonDataManager.update_entity.return_value = expected_entity

        response = self.client.patch(
            urlresolvers.reverse('person-detail', args=('John',)),
            data=json.dumps(expected_entity.__dict__),
            content_type="application/json")

        assert response.status_code == 400
        assert 'name' in json.loads(response.content)
