from django.conf.urls import url, include
from django.core import urlresolvers
from django.test import override_settings
from tests.integration_tests.base_test_case import \
    EndToEndBaseTestCase
from tests.integration_tests.resources_for_testing import \
    PersonEntity, PersonDataManager, router

urlpatterns = [
    url(r'^hello/', include(router.urls)),
]


@override_settings(ROOT_URLCONF=__name__)
class DeleteCrudResourceIntegrationTest(EndToEndBaseTestCase):
    def test_should_delete(self):
        expected_entity = PersonEntity(
            name='John', email="foo@bar.com", phone='1234',
            address={'city': 'bangalore', 'country': 'India'})
        PersonDataManager.get_entity_list.return_value = [expected_entity]

        response = self.client.delete(
            urlresolvers.reverse('person-detail', args=('John',)))

        assert response.status_code == 204
        assert PersonDataManager.delete_entity.call_count == 1
        call_args = PersonDataManager.delete_entity.call_args[0][1]
        assert call_args.__dict__ == expected_entity.__dict__

    def test_should_return_NotFound_for_non_existing_object(self):

        PersonDataManager.get_entity_list.return_value = []

        response = self.client.delete(
            urlresolvers.reverse('person-detail', args=('John',)))

        assert response.status_code == 404

    def test_should_return_NotFound_for_non_existing_object_by_param(self):

        PersonDataManager.get_entity_list.return_value = []

        response = self.client.delete(
            urlresolvers.reverse('person-detail', args=('John',)),
            data={'nick_names': 'papa'})

        assert response.status_code == 404
        call_args = PersonDataManager.get_entity_list.call_args[1]
        assert call_args['id'] == 'John'
