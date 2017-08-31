import json

from django.conf.urls import url, include
from django.core import urlresolvers
from django.test import override_settings

from rip.crud.crud_actions import CrudActions
from tests import request_factory
from tests.integration_tests.person_base_test_case import \
    PersonResourceBaseTestCase
from tests.integration_tests.resources_for_testing import PersonResource, \
    PersonDataManager
from tests.integration_tests.resources_for_testing import \
    router

urlpatterns = [
    url(r'^hello/', include(router.urls)),
]


@override_settings(ROOT_URLCONF=__name__)
class GetCountsCrudResourceIntegrationTest(PersonResourceBaseTestCase):
    def test_should_get_aggregates_by_allowed_fields(self):
        PersonDataManager.get_entity_aggregates.return_value = \
            expected_aggregates = \
            [{'name': 'asdf', 'count': 2}, {'name': 'asdf1', 'count': 10}]

        response = self.client.get(urlresolvers.reverse('person-aggregates'),
                                   data={'aggregate_by': 'name'})

        assert response.status_code == 200
        assert json.loads(response.content) == expected_aggregates

    def test_should_throw_for_disallowed_aggregates_fields(self):
        PersonDataManager.get_entity_aggregates.return_value = \
            expected_aggregates = \
            [{'name': 'asdf', 'count': 2}, {'name': 'asdf1', 'count': 10}]

        response = self.client.get(urlresolvers.reverse('person-aggregates'),
                                   data={'aggregate_by': 'email'})

        assert response.status_code == 400

    def test_should_throw_if_aggregates_fields_not_specified(self):
        PersonDataManager.get_entity_aggregates.return_value = \
            expected_aggregates = \
            [{'name': 'asdf', 'count': 2}, {'name': 'asdf1', 'count': 10}]

        response = self.client.get(urlresolvers.reverse('person-aggregates'))
        assert response.status_code == 400
        assert json.loads(response.content)['__all__'] == \
            'Aggregating requires a field'
