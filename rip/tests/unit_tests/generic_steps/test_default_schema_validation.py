import unittest
from rip.crud.crud_actions import CrudActions
from rip.crud.crud_resource import CrudResource
from rip.generic_steps import error_types
from rip.generic_steps.default_schema_validation import \
    DefaultSchemaValidation
from rip.schema_fields.boolean_field import \
    BooleanField
from rip.schema_fields.schema_field import SchemaField
from rip.schema_fields.string_field import StringField
from tests import request_factory

__all__ = ['TestSchemaFullValidation', 'TestSchemaPartialValidation']


class TestSchemaFullValidation(unittest.TestCase):
    def setUp(self):
        class RelatedResource(CrudResource):
            email = StringField(max_length=10)

        self.RelatedSchema = RelatedResource

        class TestResource(CrudResource):
            name = StringField(max_length=5, required=True)
            is_active = BooleanField(required=True)
            country = StringField(required=False, max_length=5)
            related = SchemaField(of_type=self.RelatedSchema)

        self.TestResource = TestResource
        self.validation = DefaultSchemaValidation(resource=self.TestResource())

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
        assert return_request == request

    def test_schema_validation_passes_with_required_fields(self):
        data = {
            'name': 'John',
            'is_active': True,
        }
        request = request_factory.get_request(
            data=data,
            context_params={'crud_action': CrudActions.UPDATE_DETAIL})
        return_request = self.validation.validate_request_data(request)
        assert return_request == request

    def test_raises_bad_request_if_required_data_is_missing(self):
        data = {}
        request = request_factory.get_request(
            data=data,
            context_params={'crud_action': CrudActions.CREATE_DETAIL})

        response = self.validation.validate_request_data(request)

        assert not response.is_success
        assert response.reason == error_types.InvalidData
        assert len(response.data) == 2
        assert 'name' in response.data
        assert 'is_active' in response.data

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

        assert not response.is_success
        assert response.reason == error_types.InvalidData
        assert len(response.data) == 2
        assert 'name' in response.data
        assert 'country' in response.data

    def test_input_data_is_not_a_dict(self):
        data = 'stupid random data'
        request = request_factory.get_request(
            data=data,
            context_params={'crud_action': CrudActions.UPDATE_DETAIL})

        response = self.validation.validate_request_data(request)

        assert not response.is_success
        assert response.reason == error_types.InvalidData


class TestSchemaPartialValidation(unittest.TestCase):
    class TestResource(CrudResource):
        name = StringField(max_length=5, required=True)
        is_active = BooleanField(required=True)
        country = StringField(required=False, max_length=5)

    def setUp(self):
        self.validation = DefaultSchemaValidation(resource=self.TestResource())

    def test_schema_validation_passes_with_some_fields(self):
        data = {
            'country': 'India'
        }

        request = request_factory.get_request(
            data=data, context_params={
                'crud_action': CrudActions.UPDATE_DETAIL})
        return_request = self.validation.validate_request_data(request)

        assert return_request == request

    def test_schema_validation_fails_for_wrong_datatype(self):
        data = {
            'country': 1
        }
        request = request_factory.get_request(data=data,
                                              context_params={
                                                  'crud_action': CrudActions.UPDATE_DETAIL})
        response = self.validation.validate_request_data(request)
        assert not response.is_success
        assert 'country' in response.data
