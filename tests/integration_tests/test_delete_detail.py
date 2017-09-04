from hamcrest import assert_that, equal_to
from mock import patch

from rip import error_types
from tests import request_factory
from tests.integration_tests.person_base_test_case import \
    PersonResourceBaseTestCase
from tests.integration_tests.person_resource import PersonResource, PersonEntity


class DeleteCrudResourceIntegrationTest(PersonResourceBaseTestCase):
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