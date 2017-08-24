
from mock import patch

from rip.crud.crud_actions import CrudActions
from rip.generic_steps import error_types
from tests import request_factory
from tests.integration_tests.person_base_test_case import \
    PersonResourceBaseTestCase
from tests.integration_tests.person_resource import PersonResource, PersonEntity


class DeleteCrudResourceIntegrationTest(PersonResourceBaseTestCase):
    @patch.object(PersonResource._meta.data_manager_cls, 'delete_entity')
    @patch.object(PersonResource._meta.data_manager_cls, 'get_entity_list')
    def test_should_delete(self, get_person_entity_list, delete_person_entity):
        resource = PersonResource()
        expected_entity = PersonEntity(
            name='John', email="foo@bar.com", phone='1234',
            address={'city': 'bangalore', 'country': 'India'})

        get_person_entity_list.return_value = [expected_entity]
        request = request_factory.get_request(
            user=object(), request_params={'name': 'John'})

        response = resource.run_crud_action(CrudActions.DELETE_DETAIL, request)

        assert response.is_success
        delete_person_entity.assert_called_once_with(
            request, expected_entity)

    @patch.object(PersonResource._meta.data_manager_cls, 'delete_entity')
    @patch.object(PersonResource._meta.data_manager_cls, 'get_entity_list')
    def test_should_return_NotFound_for_non_existing_object(
            self, get_person_entity_list, delete_person_entity):

        resource = PersonResource()
        get_person_entity_list.return_value = []
        request = request_factory.get_request(user=object(),
                                              request_params={'name': 'John'})

        response = resource.run_crud_action(CrudActions.DELETE_DETAIL, request)

        assert not response.is_success
        assert response.reason == error_types.ObjectNotFound
