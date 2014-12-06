import unittest

from mock import patch
from hamcrest import has_entry
from hamcrest.core import assert_that
from hamcrest.core.core.isequal import equal_to
from hamcrest.library.collection.issequence_containing import has_item

from tests import request_factory
from tests.integration_tests.person_resource import \
    PersonResource, PersonEntity, CompanyResource, FriendResource
from rip import error_types


class GetCrudResourceIntegrationTest(unittest.TestCase):
    def test_should_get_fields(self):
        resource = PersonResource()
        entity_actions = resource.configuration['entity_actions']
        expected_entities = [PersonEntity(name='John', email=None, phone='1234',
                                          address={'city': 'bangalore',
                                                   'country': 'India'},
                                          company=None, nick_names=['Johnny', 'Papa'])]
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
                                          company=None, nick_names=['Johnny', 'Papa'])]
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
        expected_company = {'name': 'Acme', 'registration_number': 12,
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
            dict(name='John', email=None, phone='1234', address=None, nick_names=['Johnny', 'Papa'])]

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


class UpdateCrudResourceIntegrationTest(unittest.TestCase):
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

    def test_should_update_fields_when_nullable_fields_not_present(self):
        resource = PersonResource()
        entity_actions = resource.configuration['entity_actions']
        expected_entity = PersonEntity(name='John', email="div@kar.com",
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
        assert_that(response.data, equal_to(expected_data))

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


class CreateCrudResourceIntegrationTest(unittest.TestCase):
    @patch.object(PersonResource.entity_actions_cls, 'create_entity')
    def test_should_create(self, create_person_entity):
        resource = PersonResource()
        expected_entity = PersonEntity(name='John', email="foo@bar.com",
                                       phone='1234',
                                       address={'city': 'bangalore',
                                                'country': 'India'},
                                       nick_names=['Johnny', 'Papa'])

        create_person_entity.return_value = expected_entity
        request = request_factory.get_request(user=object(),
                                              data=expected_entity.__dict__)

        response = resource.create_detail(request)

        assert_that(response.is_success, equal_to(True))
        expected_data = expected_entity.__dict__
        expected_data.update(friends=[])
        expected_data.update(company=None)
        assert_that(response.data, equal_to(expected_data))
        expected_update_kwargs = dict(name='John',
                                      email="foo@bar.com",
                                      address={'country': 'India'},
                                      nick_names=['Johnny', 'Papa']
        )
        create_person_entity.assert_called_once_with(
            request,
            **expected_update_kwargs)

    def test_create_with_missing_required_fields(self):
        resource = PersonResource()
        request = request_factory.get_request(user=object(),
                                              data={'email': 'foo@bar.com'})

        response = resource.create_detail(request)

        assert_that(response.is_success, equal_to(False))
        assert_that(response.data, has_entry('name', 'This field is required'))

    def test_create_with_null_for_non_nullable_field(self):
        resource = PersonResource()
        request = request_factory.get_request(user=object(),
                                              data={'name': None})

        response = resource.create_detail(request)

        assert_that(response.is_success, equal_to(False))
        assert_that(response.data,
                    has_entry('name', 'null is not a valid value'))

    @patch.object(PersonResource.entity_actions_cls, 'create_entity')
    def test_readonly_fields_are_skipped_when_calling_create_entity(
            self,
            create_person_entity):
        resource = PersonResource()
        expected_entity = PersonEntity(name='John', email="foo@bar.com",
                                       phone='1234',
                                       address={'city': 'bangalore',
                                                'country': 'India'},
                                       company='foo company',
                                       nick_names=['Johnny', 'Papa'])

        create_person_entity.return_value = expected_entity
        request = request_factory.get_request(user=object(),
                                              data=expected_entity.__dict__)

        response = resource.create_detail(request)

        assert_that(response.is_success, equal_to(True))

        expected_update_kwargs = dict(name='John',
                                      email="foo@bar.com",
                                      address={'country': 'India'},
                                      nick_names=['Johnny', 'Papa'])
        create_person_entity.assert_called_once_with(
            request,
            **expected_update_kwargs)


class DeleteCrudResourceIntegrationTest(unittest.TestCase):
    @patch.object(PersonResource.entity_actions_cls, 'delete_entity')
    @patch.object(PersonResource.entity_actions_cls, 'get_entity_list')
    def test_should_delete(self, get_person_entity_list, delete_person_entity):
        resource = PersonResource()
        expected_entity = PersonEntity(name='John', email="foo@bar.com",
                                       phone='1234',
                                       address={'city': 'bangalore',
                                                'country': 'India'})

        get_person_entity_list.return_value = [expected_entity]
        request = request_factory.get_request(user=object(),
                                              request_params={'name': 'John'})

        response = resource.delete_detail(request)

        assert_that(response.is_success, equal_to(True))
        expected_delete_kwargs = dict(name='John')
        delete_person_entity.assert_called_once_with(
            request, expected_entity)

    @patch.object(PersonResource.entity_actions_cls, 'delete_entity')
    @patch.object(PersonResource.entity_actions_cls, 'get_entity_list')
    def test_should_return_NotFound_for_non_existing_object(
            self,
            get_person_entity_list, delete_person_entity):
        resource = PersonResource()
        get_person_entity_list.return_value = []
        request = request_factory.get_request(user=object(),
                                              request_params={'name': 'John'})

        response = resource.delete_detail(request)

        assert_that(response.is_success, equal_to(False))
        assert_that(response.reason, error_types.ObjectNotFound)


class ListCrudResourceIntegrationTest(unittest.TestCase):
    def test_should_get_list(self):
        resource = PersonResource()
        entity_actions = resource.configuration['entity_actions']
        expected_entities = [PersonEntity(name='John', email=None, phone='1234',
                                          address={'city': 'bangalore',
                                                   'country': 'India'},
                                          company=None, nick_names=['Johnny', 'Papa'])]
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
                                          company=None, nick_names=['Johnny', 'Papa'])]
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
                                          company=None, nick_names=['Johnny', 'Papa'])]

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
                                          company=None, nick_names=['Johnny', 'Papa'])]

        entity_actions.get_entity_list.return_value = expected_entities
        entity_actions.get_entity_list_total_count.return_value = 1
        user = object()
        request = request_factory.get_request(user=user, request_params={
            'nick_names': 'Johnny'})

        response = resource.read_list(request)
        assert response.is_success is True
        assert 'Johnny' in response.data['objects'][0]['nick_names']


class GetCountsCrudResourceIntegrationTest(unittest.TestCase):
    def test_should_get_aggregates_by_allowed_fields(self):
        resource = PersonResource()
        entity_actions = resource.configuration['entity_actions']
        entity_actions.get_entity_aggregates.return_value = \
            expected_aggregates = \
            [{'name': 'asdf', 'count': 2}, {'name': 'asdf1', 'count': 10}]
        user = object()
        request = request_factory.get_request(user=user, request_params={
            'aggregate_by': 'name'})

        response = resource.get_aggregates(request)

        assert response.is_success is True
        assert response.data == expected_aggregates
