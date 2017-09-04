from hamcrest import assert_that, equal_to

from mock import patch

from tests import request_factory

from tests.integration_tests.person_base_test_case import \
    PersonResourceBaseTestCase
from tests.integration_tests.person_resource import PersonResource, \
    PersonEntity, \
    FriendResource, CompanyResource


class GetCrudResourceIntegrationTest(PersonResourceBaseTestCase):
    def test_should_get_fields(self):
        resource = PersonResource()
        entity_actions = resource.configuration['entity_actions']
        expected_entities = [PersonEntity(name='John', email=None, phone='1234',
                                          address={'city': 'bangalore',
                                                   'country': 'India'},
                                          company=None,
                                          nick_names=['Johnny', 'Papa'])]
        entity_actions.get_entity_list.return_value = expected_entities
        request = request_factory.get_request(user=object())

        response = resource.read_detail(request, )

        assert_that(response.is_success, equal_to(True))
        expected_data = expected_entities[0].__dict__
        expected_data.update(friends=[])
        assert_that(response.data, equal_to(expected_data))

    def test_should_get_by_allowed_filters(self):
        resource = PersonResource()
        entity_actions = resource.configuration['entity_actions']
        expected_entities = [PersonEntity(name='John', email=None, phone='1234',
                                          address={'city': 'bangalore',
                                                   'country': 'India'},
                                          company=None,
                                          nick_names=['Johnny', 'Papa'])]
        entity_actions.get_entity_list.return_value = expected_entities
        request = request_factory.get_request(user=object(),
                                              request_params={'name': 'bar'})

        response = resource.read_detail(request)

        assert_that(response.is_success, equal_to(True))
        entity_actions.get_entity_list.assert_called_once_with(request,
                                                               name='bar')


    @patch.object(CompanyResource.entity_actions_cls, 'get_entity_list')
    def test_should_get_sub_resource(self, company_entity_list):
        resource = PersonResource()
        entity_actions = resource.configuration['entity_actions']

        expected_entities = [
            PersonEntity(
                name='John', email=None, phone='1234',
                address={'city': 'bangalore',
                         'country': 'India'}, nick_names=['Johnny', 'Papa'])
        ]
        expected_company = {
            'name': 'Acme', 'registration_number': 12,
            'resource_uri': '/api/v2/persons/John/companies/Acme/'}
        expected_companies = [expected_company]
        company_entity_list.return_value = expected_companies
        entity_actions.get_entity_list.return_value = expected_entities
        request = request_factory.get_request(user=object())
        response = resource.read_detail(request)

        assert_that(response.is_success, equal_to(True))
        assert_that(response.data['company'], equal_to(expected_company))

    @patch.object(FriendResource.entity_actions_cls, 'get_entity_list')
    @patch.object(FriendResource.entity_actions_cls,
                  'get_entity_list_total_count')
    def test_should_get_list_sub_resource(self, friend_entity_count,
                                          friend_entity_list):
        resource = PersonResource()
        entity_actions = resource.configuration['entity_actions']

        expected_persons = [
            dict(name='John', email=None, phone='1234', address=None,
                 nick_names=['Johnny', 'Papa'])]

        friend1 = dict(name='friend1', relationship_type='platonic')
        friend2 = dict(name='friend2', relationship_type='girlfriend')

        friend_entity_list.return_value = [friend1, friend2]
        friend_entity_count.return_value = 2
        entity_actions.get_entity_list.return_value = expected_persons
        request = request_factory.get_request(user=object())
        response = resource.read_detail(request)

        assert_that(response.is_success, equal_to(True))
        friend1.update(resource_uri=u'/api/v2/persons/John/friends/friend1/')
        friend2.update(resource_uri=u'/api/v2/persons/John/friends/friend2/')
        expected_friends = [friend1, friend2]
        assert_that(response.data['friends'], equal_to(expected_friends))

    def test_should_get_none_for_nullable_schema_field(self):
        resource = PersonResource()
        entity_actions = resource.configuration['entity_actions']
        expected_entities = [PersonEntity(name='John', email=None,
                                          phone='1234',
                                          address=None, company=None,
                                          nick_names=['Johnny', 'Papa'])]
        entity_actions.get_entity_list.return_value = expected_entities
        request = request_factory.get_request(user=object())

        response = resource.read_detail(request, )

        assert_that(response.is_success, equal_to(True))
        expected_data = expected_entities[0].__dict__
        expected_data.update(friends=[])
        assert_that(response.data, equal_to(expected_data))