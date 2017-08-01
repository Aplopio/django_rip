from hamcrest import assert_that, equal_to

from rip.generic_steps import error_types
from tests import request_factory
from tests.integration_tests.person_base_test_case import \
    PersonResourceBaseTestCase
from tests.integration_tests.person_resource import PersonResource, PersonEntity


class ListCrudResourceIntegrationTest(PersonResourceBaseTestCase):
    def test_should_get_list(self):
        resource = PersonResource()
        entity_actions = resource.configuration['entity_actions']
        expected_entities = [PersonEntity(name='John', email=None, phone='1234',
                                          address={'city': 'bangalore',
                                                   'country': 'India'},
                                          company=None,
                                          nick_names=['Johnny', 'Papa'])]
        entity_actions.get_entity_list.return_value = expected_entities
        entity_actions.get_entity_list_total_count.return_value = 1
        request = request_factory.get_request(user=object())

        response = resource.read_list(request)

        assert_that(response.is_success, equal_to(True))
        expected_entity = expected_entities[0].__dict__.copy()
        expected_entity.pop('company')
        expected_data = [expected_entity]
        assert_that(response.data['objects'], equal_to(expected_data))
        assert_that(response.data['meta']['total'], equal_to(1))

    def test_should_get_list_fields_only(self):
        resource = PersonResource()
        entity_actions = resource.configuration['entity_actions']
        expected_entities = [PersonEntity(name='John', email=None, phone='1234',
                                          address={'city': 'bangalore',
                                                   'country': 'India'},
                                          company=None,
                                          nick_names=['Johnny', 'Papa'])]
        entity_actions.get_entity_list.return_value = expected_entities
        entity_actions.get_entity_list_total_count.return_value = 1
        request = request_factory.get_request(user=object())

        response = resource.read_list(request)

        assert_that(response.is_success, equal_to(True))
        response_data = response.data['objects'][0]
        self.assertTrue('company' not in response_data)

    def test_should_fail_ordering_by_non_order_by_fields(self):
        resource = PersonResource()
        entity_actions = resource.configuration['entity_actions']
        expected_entities = [PersonEntity(name='John', email=None, phone='1234',
                                          address={'city': 'bangalore',
                                                   'country': 'India'},
                                          company=None)]

        entity_actions.get_entity_list.return_value = expected_entities
        entity_actions.get_entity_list_total_count.return_value = 1
        user = object()
        request = request_factory.get_request(user=user, request_params={
            'order_by': 'email'})

        response = resource.read_list(request)

        assert response.is_success is False
        assert response.reason is error_types.InvalidData
        assert ('email', 'Ordering not allowed') in response.data.items()

    def test_should_order_by_allowed_field(self):
        resource = PersonResource()
        entity_actions = resource.configuration['entity_actions']
        expected_entities = [PersonEntity(name='John', email=None, phone='1234',
                                          address={'city': 'bangalore',
                                                   'country': 'India'},
                                          company=None,
                                          nick_names=['Johnny', 'Papa'])]

        entity_actions.get_entity_list.return_value = expected_entities
        entity_actions.get_entity_list_total_count.return_value = 1
        user = object()
        request = request_factory.get_request(user=user, request_params={
            'order_by': 'name'})

        response = resource.read_list(request)
        assert response.is_success is True

    def test_should_filter_by_list_field(self):
        resource = PersonResource()
        entity_actions = resource.configuration['entity_actions']
        expected_entities = [PersonEntity(name='John', email=None, phone='1234',
                                          address={'city': 'bangalore',
                                                   'country': 'India'},
                                          company=None,
                                          nick_names=['Johnny', 'Papa'])]

        entity_actions.get_entity_list.return_value = expected_entities
        entity_actions.get_entity_list_total_count.return_value = 1
        user = object()
        request = request_factory.get_request(user=user, request_params={
            'nick_names': 'Johnny'})

        response = resource.read_list(request)
        assert response.is_success is True
        assert 'Johnny' in response.data['objects'][0]['nick_names']