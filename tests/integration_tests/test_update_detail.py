from rip.crud.crud_actions import CrudActions
from rip.generic_steps import error_types
from tests import request_factory
from tests.integration_tests.person_base_test_case import \
    PersonResourceBaseTestCase
from tests.integration_tests.person_resource import PersonResource, PersonEntity


class UpdateCrudResourceIntegrationTest(PersonResourceBaseTestCase):
    def test_should_update_fields(self):
        resource = PersonResource()
        data_manager = resource.data_manager
        expected_entity = PersonEntity(name='John', email="foo@bar.com",
                                       phone='1234',
                                       address={'city': 'bangalore',
                                                'country': 'India'},
                                       company=None,
                                       nick_names=['Johnny', 'Papa'])

        data_manager.get_entity_list.return_value = [expected_entity]
        data_manager.update_entity.return_value = expected_entity
        request = request_factory.get_request(user=object(),
                                              data=expected_entity.__dict__)

        response = resource.run_crud_action(CrudActions.UPDATE_DETAIL, request)

        assert response.is_success
        expected_data = expected_entity.__dict__
        assert response.data == expected_data
        expected_update_kwargs = expected_data.copy()
        expected_update_kwargs.pop('phone')
        expected_update_kwargs['address'].pop('city')
        data_manager.update_entity.assert_called_once_with(
            request, expected_entity,
            **expected_update_kwargs)

    def test_success_when_nullable_fields_set_to_none(self):
        resource = PersonResource()
        data_manager = resource.data_manager
        expected_entity = PersonEntity(name='John', email=None,
                                       phone='1234',
                                       address=None, company=None,
                                       nick_names=['Johnny', 'Papa'])

        data_manager.get_entity_list.return_value = [expected_entity]
        data_manager.update_entity.return_value = expected_entity
        request = request_factory.get_request(user=object(),
                                              data=expected_entity.__dict__)

        response = resource.run_crud_action(CrudActions.UPDATE_DETAIL, request)

        assert response.is_success
        expected_data = expected_entity.__dict__
        expected_data.update(email=None)
        assert response.data == expected_data

    def test_success_when_one_required_fields_are_not_present(self):
        resource = PersonResource()
        data_manager = resource.data_manager
        expected_entity = PersonEntity(email=None,
                                       phone='1234',
                                       address=None, company=None,
                                       nick_names=['Johnny', 'Papa'])

        data = expected_entity.__dict__
        expected_entity.name = 'John'
        data_manager.get_entity_list.return_value = [expected_entity]
        data_manager.update_entity.return_value = expected_entity
        request = request_factory.get_request(user=object(),
                                              data=data)

        response = resource.run_crud_action(CrudActions.UPDATE_DETAIL, request)

        assert response.is_success
        assert response.data == expected_entity.__dict__

    def test_update_when_non_nullable_fields_are_set_to_none(self):
        resource = PersonResource()
        data_manager = resource.data_manager
        expected_entity = PersonEntity(name=None, email=None,
                                       phone='1234',
                                       address=None, company=None)

        data_manager.get_entity_list.return_value = [expected_entity]
        data_manager.update_entity.return_value = expected_entity
        request = request_factory.get_request(user=object(),
                                              data=expected_entity.__dict__)

        response = resource.run_crud_action(CrudActions.UPDATE_DETAIL, request)

        assert not response.is_success
        assert response.reason == error_types.InvalidData
        assert 'name' in response.data
