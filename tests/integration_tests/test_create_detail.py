import json

from django.conf.urls import url, include
from django.core import urlresolvers
from django.test import override_settings

from tests.integration_tests.person_base_test_case import \
    PersonResourceBaseTestCase
from tests.integration_tests.resources_for_testing import (
    PersonEntity, router, PersonDataManager)

urlpatterns = [
    url(r'^hello/', include(router.urls)),
]


@override_settings(ROOT_URLCONF=__name__)
class CrudResourceCreateActionIntegrationTest(PersonResourceBaseTestCase):
    def test_should_create(self):
        expected_entity = PersonEntity(name='John', email="foo@bar.com",
                                       phone='1234',
                                       address={'city': 'bangalore',
                                                'country': 'India'},
                                       nick_names=['Johnny', 'Papa'])

        create_entity_fn = PersonDataManager.create_entity
        create_entity_fn.return_value = expected_entity

        response = self.client.post(urlresolvers.reverse('person-list'),
                                    data=json.dumps(expected_entity.__dict__),
                                    content_type="application/json")

        assert response.status_code == 201
        expected_data = expected_entity.__dict__
        assert json.loads(response.content) == expected_data
        expected_update_kwargs = dict(
            name='John', email="foo@bar.com", address={'country': 'India'},
            nick_names=['Johnny', 'Papa'])
        assert create_entity_fn.call_count == 1
        # first call arg is the request object, the rest of
        # kwargs gets captured as second param
        call_kwargs = create_entity_fn.call_args[1]
        assert call_kwargs == expected_update_kwargs

    def test_create_with_missing_required_fields(self):
        post_data = {'email': 'foo@bar.com'}
        response = self.client.post(urlresolvers.reverse('person-list'),
                                    data=json.dumps(post_data),
                                    content_type="application/json")

        assert response.status_code == 400
        response_data = json.loads(response.content)
        assert response_data.get('name') == 'This field is required'

    def test_create_with_blank_fields(self):
        post_data = {'name': ''}
        response = self.client.post(urlresolvers.reverse('person-list'),
                                    data=json.dumps(post_data),
                                    content_type="application/json")

        assert response.status_code == 400
        response_data = json.loads(response.content)
        assert response_data.get('name') == 'This field is required'

    def test_create_with_null_for_non_nullable_field(self):
        post_data = {'name': None}
        response = self.client.post(urlresolvers.reverse('person-list'),
                                    data=json.dumps(post_data),
                                    content_type="application/json")

        assert response.status_code == 400
        response_data = json.loads(response.content)
        assert response_data.get('name') == 'null is not a valid value'

    def test_readonly_fields_are_skipped_when_calling_create_entity(self):
        expected_entity = PersonEntity(
            name='John', email="foo@bar.com",
            phone='1234', address={'city': 'bangalore', 'country': 'India'},
            company='foo company', nick_names=['Johnny', 'Papa'])

        PersonDataManager.create_entity.return_value = expected_entity
        response = self.client.post(urlresolvers.reverse('person-list'),
                                    data=json.dumps(expected_entity.__dict__),
                                    content_type="application/json")

        assert response.status_code == 201
        expected_kwargs = expected_entity.__dict__.copy()
        expected_kwargs.pop('phone')
        expected_kwargs['address'].pop('city')
        assert PersonDataManager.create_entity.call_count == 1
        call_kwargs = PersonDataManager.create_entity.call_args[1]
        assert call_kwargs == expected_kwargs
