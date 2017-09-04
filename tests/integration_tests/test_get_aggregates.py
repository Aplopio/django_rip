from tests import request_factory
from tests.integration_tests.person_base_test_case import \
    PersonResourceBaseTestCase
from tests.integration_tests.person_resource import PersonResource


class GetCountsCrudResourceIntegrationTest(PersonResourceBaseTestCase):
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