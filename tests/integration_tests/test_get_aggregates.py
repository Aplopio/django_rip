from rip.crud.crud_actions import CrudActions
from tests import request_factory
from tests.integration_tests.person_base_test_case import \
    PersonResourceBaseTestCase
from tests.integration_tests.person_resource import PersonResource


class GetCountsCrudResourceIntegrationTest(PersonResourceBaseTestCase):
    def test_should_get_aggregates_by_allowed_fields(self):
        resource = PersonResource()
        data_manager = resource.data_manager
        data_manager.get_entity_aggregates.return_value = \
            expected_aggregates = \
            [{'name': 'asdf', 'count': 2}, {'name': 'asdf1', 'count': 10}]
        user = object()
        request = request_factory.get_request(user=user, request_params={
            'aggregate_by': 'name'})

        response = resource.run_crud_action(CrudActions.GET_AGGREGATES, request)

        assert response.is_success is True
        assert response.data == expected_aggregates
