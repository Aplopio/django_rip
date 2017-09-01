import json

from django.conf.urls import url, include
from django.core import urlresolvers
from django.test import override_settings

from tests.integration_tests.base_test_case import \
    EndToEndBaseTestCase
from tests.integration_tests.resources_for_testing import \
    router, FriendEntity, FriendDataManager

urlpatterns = [
    url(r'^hello/', include(router.urls)),
]


@override_settings(ROOT_URLCONF=__name__)
class SubResourceIntegrationTest(EndToEndBaseTestCase):
    def test_should_get_list(self):
        expected_entities = [FriendEntity(name='Friend',
                                          relationship_type='acquaintance',
                                          person_id=2)]

        FriendDataManager.get_entity_list.return_value = expected_entities
        FriendDataManager.get_entity_list_total_count.return_value = 1

        response = self.client.get(urlresolvers.reverse(
            'friend-list', kwargs={'person_id': 2}))

        assert response.status_code == 200
        expected_entity = expected_entities[0].__dict__.copy()
        expected_entity['resource_uri'] = '/hello/person/2/friend/Friend/'
        expected_data = [expected_entity]
        response_data = json.loads(response.content)
        assert response_data['objects'] == expected_data
        assert response_data['meta']['total'] == 1

    def test_should_pass_parent_id(self):
        expected_entities = [FriendEntity(name='Friend',
                                          relationship_type='acquaintance',
                                          person_id=2, id="Friend")]
        FriendDataManager.get_entity_list.return_value = expected_entities
        FriendDataManager.get_entity_list_total_count.return_value = 1

        response = self.client.get(
            urlresolvers.reverse('friend-list', args=(2,)))

        assert response.status_code == 200
        call_args = FriendDataManager.get_entity_list.call_args[1]
        assert call_args['person_id'] == '2'

    def test_should_pass_filter_by_attributes(self):
        expected_entities = [FriendEntity(name='Friend',
                                          relationship_type='acquaintance',
                                          person_id=2, id="Friend")]
        FriendDataManager.get_entity_list.return_value = expected_entities
        FriendDataManager.get_entity_list_total_count.return_value = 1

        response = self.client.get(
            urlresolvers.reverse('friend-list', args=(2,)),
            data={'relationship_type': 'acquaintance'})

        assert response.status_code == 200
        call_args = FriendDataManager.get_entity_list.call_args[1]
        assert call_args['relationship_type'] == 'acquaintance'

    def test_should_get_entity(self):
        expected_entities = [FriendEntity(name='Friend',
                                          relationship_type='acquaintance',
                                          person_id=2)]
        FriendDataManager.get_entity_list.return_value = expected_entities
        FriendDataManager.get_entity_list_total_count.return_value = 1

        response = self.client.get(
            urlresolvers.reverse('friend-detail',
                                 kwargs=dict(person_id=2, name=4)))

        assert response.status_code == 200
        response_content = json.loads(response.content)
        assert response_content['resource_uri'] == \
            '/hello/person/2/friend/Friend/'
        call_args = FriendDataManager.get_entity_list.call_args[1]
        assert call_args['name'] == '4'
        assert call_args['person_id'] == '2'

    def test_update_entity(self):
        entity = FriendEntity(name='Friend',
                              relationship_type='acq',
                              person_id='2',
                              resource_uri='/hello/person/2/friend/Friend')
        expected_entities = [entity]
        FriendDataManager.get_entity_list.return_value = expected_entities
        FriendDataManager.get_entity_list_total_count.return_value = 1
        FriendDataManager.update_entity.return_value = expected_entities[0]

        response = self.client.patch(
            urlresolvers.reverse('friend-detail',
                                 kwargs=dict(person_id=2, name=4)),
            data=json.dumps(entity.__dict__),
            content_type='application/json'
        )

        assert response.status_code == 202
        call_args = FriendDataManager.update_entity.call_args[1]
        expected_call_args = entity.__dict__.copy()
        expected_call_args.pop('resource_uri')
        assert call_args == expected_call_args

    def test_delete_entity(self):
        entity = FriendEntity(name='Friend',
                              relationship_type='acq',
                              person_id='2',
                              resource_uri='/hello/person/2/friend/Friend')
        expected_entities = [entity]
        FriendDataManager.get_entity_list.return_value = expected_entities
        FriendDataManager.get_entity_list_total_count.return_value = 1
        FriendDataManager.delete_entity.return_value = None

        response = self.client.delete(
            urlresolvers.reverse('friend-detail',
                                 kwargs=dict(person_id=2, name=4)),)

        assert response.status_code == 204
