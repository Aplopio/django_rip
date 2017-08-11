from hamcrest import assert_that, equal_to, has_entry
from mock import patch

from rip.crud.crud_actions import CrudActions
from tests import request_factory
from tests.integration_tests.person_base_test_case import \
    PersonResourceBaseTestCase
from tests.integration_tests.person_resource import (
    PersonResource, PersonEntity, )
from tests.integration_tests.blank_test_resource import BlankTestResource


class CrudResourceCreateActionIntegrationTest(PersonResourceBaseTestCase):
    @patch.object(PersonResource.EntityActions, 'create_entity')
    def test_should_create(self, create_person_entity):
        resource = PersonResource()
        expected_entity = PersonEntity(name='John', email="foo@bar.com",
                                       phone='1234',
                                       address={'city': 'bangalore',
                                                'country': 'India'},
                                       nick_names=['Johnny', 'Papa'])

        create_person_entity.return_value = expected_entity
        request = request_factory.get_request(
            user=object(), data=expected_entity.__dict__)

        response = resource.run_crud_action(CrudActions.CREATE_DETAIL, request)

        assert response.is_success
        expected_data = expected_entity.__dict__
        assert response.data == expected_data
        expected_update_kwargs = dict(
            name='John', email="foo@bar.com", address={'country': 'India'},
            nick_names=['Johnny', 'Papa'])
        create_person_entity.assert_called_once_with(
            request, **expected_update_kwargs)

    def test_create_with_missing_required_fields(self):
        resource = PersonResource()
        request = request_factory.get_request(
            user=object(),
            data={'email': 'foo@bar.com'})

        response = resource.run_crud_action(CrudActions.CREATE_DETAIL, request)

        assert not response.is_success
        assert response.data.get('name') == 'This field is required'

    def test_create_with_blank_fields(self):
        resource = BlankTestResource()
        request = request_factory.get_request(user=object(),
                                              data={'name': ''})

        response = resource.run_crud_action(CrudActions.CREATE_DETAIL, request)

        assert response.is_success is False
        assert response.data['name'] == 'This field is required'

    def test_create_with_null_for_non_nullable_field(self):
        resource = PersonResource()
        request = request_factory.get_request(user=object(),
                                              data={'name': None})

        response = resource.run_crud_action(CrudActions.CREATE_DETAIL, request)

        assert not response.is_success
        assert response.data.get('name') == 'null is not a valid value'

    @patch.object(PersonResource.EntityActions, 'create_entity')
    def test_readonly_fields_are_skipped_when_calling_create_entity(
            self, create_person_entity):
        resource = PersonResource()
        expected_entity = PersonEntity(
            name='John', email="foo@bar.com",
            phone='1234', address={'city': 'bangalore', 'country': 'India'},
            company='foo company', nick_names=['Johnny', 'Papa'])

        create_person_entity.return_value = expected_entity
        request = request_factory.get_request(user=object(),
                                              data=expected_entity.__dict__)

        response = resource.run_crud_action(CrudActions.CREATE_DETAIL, request)

        assert response.is_success

        expected_update_kwargs = dict(name='John',
                                      email="foo@bar.com",
                                      address={'country': 'India'},
                                      nick_names=['Johnny', 'Papa'])
        create_person_entity.assert_called_once_with(
            request,
            **expected_update_kwargs)
