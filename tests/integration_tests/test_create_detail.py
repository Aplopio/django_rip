from hamcrest import assert_that, equal_to, has_entry
from mock import patch

from tests import request_factory
from tests.integration_tests.person_base_test_case import \
    PersonResourceBaseTestCase
from tests.integration_tests.person_resource import PersonResource, PersonEntity


class CreateCrudResourceIntegrationTest(PersonResourceBaseTestCase):
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