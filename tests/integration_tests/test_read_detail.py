from mock import patch

from rip.crud.crud_actions import CrudActions
from tests import request_factory
from tests.integration_tests.person_base_test_case import \
    PersonResourceBaseTestCase
from tests.integration_tests.person_resource import PersonResource, \
    PersonEntity, \
    FriendResource, CompanyResource


class GetCrudResourceIntegrationTest(PersonResourceBaseTestCase):
    def test_should_get_fields(self):
        resource = PersonResource()
        entity_actions = resource.entity_actions
        expected_entities = [PersonEntity(name='John', email=None, phone='1234',
                                          address={'city': 'bangalore',
                                                   'country': 'India'},
                                          company=None,
                                          nick_names=['Johnny', 'Papa'])]
        entity_actions.get_entity_list.return_value = expected_entities
        request = request_factory.get_request(user=object())

        response = resource.run_crud_action(CrudActions.READ_DETAIL, request)

        assert response.is_success
        expected_data = expected_entities[0].__dict__
        assert response.data == expected_data

    def test_should_get_by_allowed_filters(self):
        resource = PersonResource()
        entity_actions = resource.entity_actions
        expected_entities = [PersonEntity(name='John', email=None, phone='1234',
                                          address={'city': 'bangalore',
                                                   'country': 'India'},
                                          company=None,
                                          nick_names=['Johnny', 'Papa'])]
        entity_actions.get_entity_list.return_value = expected_entities
        request = request_factory.get_request(user=object(),
                                              request_params={'name': 'bar'})

        response = resource.run_crud_action(CrudActions.READ_DETAIL, request)

        assert response.is_success
        entity_actions.get_entity_list.assert_called_once_with(
            request, name='bar')

    def test_should_get_none_for_nullable_schema_field(self):
        resource = PersonResource()
        entity_actions = resource.entity_actions
        expected_entities = [PersonEntity(name='John', email=None,
                                          phone='1234',
                                          address=None, company=None,
                                          nick_names=['Johnny', 'Papa'])]
        entity_actions.get_entity_list.return_value = expected_entities
        request = request_factory.get_request(user=object())

        response = resource.run_crud_action(CrudActions.READ_DETAIL, request)

        assert response.is_success
        expected_data = expected_entities[0].__dict__
        assert response.data == expected_data
