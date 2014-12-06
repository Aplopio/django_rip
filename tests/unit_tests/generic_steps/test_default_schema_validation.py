import unittest

from hamcrest.core import assert_that
from hamcrest.core.core.isequal import equal_to
from hamcrest.library.collection.issequence_containing import has_item, \
    has_items

from rip.api_schema import ApiSchema
from rip.crud.crud_actions import CrudActions
from rip.generic_steps.default_schema_validation import \
    DefaultSchemaValidation
from rip.schema.boolean_field import \
    BooleanField
from rip.schema.string_field import StringField
from rip.schema.schema_field import SchemaField
from rip import error_types
from tests import request_factory


__all__ = ['TestSchemaFullValidation', 'TestSchemaPartialValidation']


class TestSchemaFullValidation(unittest.TestCase):
    def setUp(self):
        class RelatedSchema(ApiSchema):
            email = StringField(max_length=10)

        self.RelatedSchema = RelatedSchema


        class TestSchema(ApiSchema):
            name = StringField(max_length=5, required=True)
            is_active = BooleanField(required=True)
            country = StringField(required=False, max_length=5)
            related = SchemaField(of_type=self.RelatedSchema)

            class Meta:
                schema_name = 'asdf'

        self.TestSchema = TestSchema
        self.validation = DefaultSchemaValidation(schema_cls=self.TestSchema)


    def test_schema_validation_passes_with_all_fields(self):
        data = {
            'name': 'John',
            'is_active': True,
            'country': 'India'
        }
        request = request_factory.get_request(
            data=data,
            context_params={'crud_action': CrudActions.UPDATE_DETAIL})
        return_request = self.validation.validate_request_data(request)
        assert_that(return_request, equal_to(request))

    def test_schema_validation_passes_with_required_fields(self):
        data = {
            'name': 'John',
            'is_active': True,
        }
        request = request_factory.get_request(
            data=data,
            context_params={'crud_action': CrudActions.UPDATE_DETAIL})
        return_request = self.validation.validate_request_data(request)
        assert_that(return_request, equal_to(request))

    def test_raises_bad_request_if_required_data_is_missing(self):
        data = {}
        request = request_factory.get_request(
            data=data,
            context_params={'crud_action': CrudActions.CREATE_DETAIL})

        response = self.validation.validate_request_data(request)

        assert_that(response.is_success, equal_to(False))
        assert_that(response.reason, equal_to(error_types.InvalidData))
        assert_that(len(response.data), equal_to(2))
        assert_that(response.data, has_items('name', 'is_active'))

    def test_raises_bad_request_if_field_greater_than_max_length(self):
        data = {
            'name': 'John Smith',
            'is_active': True,
            'country': 'United States'
        }
        request = request_factory.get_request(
            data=data,
            context_params={'crud_action': CrudActions.UPDATE_DETAIL})
        response = self.validation.validate_request_data(request)
        assert_that(response.is_success, equal_to(False))
        assert_that(response.reason, equal_to(error_types.InvalidData))
        assert_that(len(response.data), equal_to(2))
        assert_that(response.data, has_items('name', 'country'))


    def test_validate_schema_fields(self):
        pass


class TestSchemaPartialValidation(unittest.TestCase):
    class TestSchema(ApiSchema):
        name = StringField(max_length=5, required=True)
        is_active = BooleanField(required=True)
        country = StringField(required=False, max_length=5)

        class Meta:
            schema_name = 'asdf'

    def setUp(self):
        self.validation = DefaultSchemaValidation(schema_cls=self.TestSchema)

    def test_schema_validation_passes_with_some_fields(self):
        data = {
            'country': 'India'
        }

        request = request_factory.get_request(data=data,
                                              context_params={
                                              'crud_action': CrudActions.UPDATE_DETAIL})
        return_request = self.validation.validate_request_data(request)
        assert_that(return_request, equal_to(request))

    def test_schema_validation_fails_for_wrong_datatype(self):
        data = {
            'country': 1
        }
        request = request_factory.get_request(data=data,
                                              context_params={
                                              'crud_action': CrudActions.UPDATE_DETAIL})
        response = self.validation.validate_request_data(request)
        assert_that(response.is_success, equal_to(False))
        assert_that(response.data, has_item('country'))


if __name__ == '__main__':
    unittest.main()
