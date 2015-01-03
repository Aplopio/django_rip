from hamcrest import assert_that, equal_to, has_item

from rip import error_types
from tests import request_factory
from tests.integration_tests.person_base_test_case import \
    PersonResourceBaseTestCase
from tests.integration_tests.person_resource import PersonResource, PersonEntity


class UpdateCrudResourceIntegrationTest(PersonResourceBaseTestCase):
    def test_should_update_fields(self):
        resource = PersonResource()
        entity_actions = resource.configuration['entity_actions']
        expected_entity = PersonEntity(name='John', email="foo@bar.com",
                                       phone='1234',
                                       address={'city': 'bangalore',
                                                'country': 'India'},
                                       company=None,
                                       nick_names=['Johnny', 'Papa'])

        entity_actions.get_entity_list.return_value = [expected_entity]
        entity_actions.update_entity.return_value = expected_entity
        request = request_factory.get_request(user=object(),
                                              data=expected_entity.__dict__)

        response = resource.update_detail(request)

        assert_that(response.is_success, equal_to(True))
        expected_data = expected_entity.__dict__
        expected_data.update(friends=[])
        assert_that(response.data, equal_to(expected_data))
        expected_update_kwargs = dict(name='John',
                                      email="foo@bar.com",
                                      address={'country': 'India'},
                                      nick_names=['Johnny', 'Papa'])
        entity_actions.update_entity.assert_called_once_with(
            request, expected_entity,
            **expected_update_kwargs)

    def test_success_when_nullable_fields_set_to_none(self):
        resource = PersonResource()
        entity_actions = resource.configuration['entity_actions']
        expected_entity = PersonEntity(name='John', email=None,
                                       phone='1234',
                                       address=None, company=None,
                                       nick_names=['Johnny', 'Papa'])

        entity_actions.get_entity_list.return_value = [expected_entity]
        entity_actions.update_entity.return_value = expected_entity
        request = request_factory.get_request(user=object(),
                                              data=expected_entity.__dict__)

        response = resource.update_detail(request)

        assert_that(response.is_success, equal_to(True))
        expected_data = expected_entity.__dict__
        expected_data.update(friends=[])
        expected_data.update(email=None)
        assert_that(response.data, equal_to(expected_data))

    def test_success_when_one_required_fields_are_not_present(self):
        resource = PersonResource()
        entity_actions = resource.configuration['entity_actions']
        expected_entity = PersonEntity(email=None,
                                       phone='1234',
                                       address=None, company=None,
                                       nick_names=['Johnny', 'Papa'])

        data = expected_entity.__dict__
        expected_entity.name = 'John'
        expected_entity.friends = []
        entity_actions.get_entity_list.return_value = [expected_entity]
        entity_actions.update_entity.return_value = expected_entity
        request = request_factory.get_request(user=object(),
                                              data=data)

        response = resource.update_detail(request)

        assert_that(response.is_success, equal_to(True))
        assert_that(response.data, equal_to(expected_entity.__dict__))

    def test_update_when_non_nullable_fields_are_set_to_none(self):
        resource = PersonResource()
        entity_actions = resource.configuration['entity_actions']
        expected_entity = PersonEntity(name=None, email=None,
                                       phone='1234',
                                       address=None, company=None)

        entity_actions.get_entity_list.return_value = [expected_entity]
        entity_actions.update_entity.return_value = expected_entity
        request = request_factory.get_request(user=object(),
                                              data=expected_entity.__dict__)

        response = resource.update_detail(request)

        assert_that(response.is_success, equal_to(False))
        assert_that(response.reason, equal_to(error_types.InvalidData))
        assert_that(response.data, has_item('name'))