import unittest

from rip.crud.crud_actions import CrudActions
from rip.generic_steps.default_schema_serializer import DefaultEntitySerializer
from rip.generic_steps.default_schema_validation import \
    DefaultSchemaValidation
from rip.schema.api_schema import ApiSchema
from rip.schema.schema_field import SchemaField
from rip.schema.string_field import StringField
from rip.schema.validation_result import \
    ValidationResult
from tests import request_factory


class TestSchemaField(unittest.TestCase):
    def setUp(self):
        class TestSchema(ApiSchema):
            class Meta:
                schema_name = 'test_schema'

            name = StringField(max_length=10)

        self.test_schema_cls = TestSchema

        class TestEntity(object):
            def __init__(self, name, surname):
                self.name = name
                self.surname = surname

        self.test_entity_cls = TestEntity

    def test_should_serialize_with_default_serializer(self):
        field = SchemaField(of_type=self.test_schema_cls)

        serialized_dict = field.serialize(
            request_factory.get_request(),
            self.test_entity_cls('John', 'Smith'))

        assert serialized_dict['name'] == 'John'

    def test_should_serialize_with_overridden_serializer(self):
        test_schema_cls = self.test_schema_cls
        request = request_factory.get_request(
            context_params={'crud_action': CrudActions.UPDATE_DETAIL})

        class TestSerializer(DefaultEntitySerializer):
            def serialize_entity(self, request, entity):
                return {'name': entity.surname}

        field = SchemaField(of_type=self.test_schema_cls,
                            serializer_cls=TestSerializer)

        response_dict = field.serialize(request,
                                        self.test_entity_cls('John', 'Smith'))

        assert response_dict['name'] == 'Smith'

    def test_should_validate(self):
        field = SchemaField(self.test_schema_cls)
        request = request_factory.get_request(
            context_params={'crud_action': CrudActions.UPDATE_DETAIL})
        result = field.validate(request, {'name': 1})

        assert isinstance(result, ValidationResult)
        assert not result.is_success
        assert result.reason.get('name') == 'Expected type string'

    def test_should_validate_with_overridden_validator(self):
        class TestValidator(DefaultSchemaValidation):
            def __init__(self, schema_cls):
                super(TestValidator, self).__init__(schema_cls)

            def validate_data(self, data, fields_to_validate=None):
                return {'name': 'Custom Validation Failed'}

        field = SchemaField(of_type=self.test_schema_cls,
                            validator_cls=TestValidator)

        result = field.validate(None, {'name': 1})

        assert isinstance(result, ValidationResult)
        assert not result.is_success
        assert result.reason.get('name') == 'Custom Validation Failed'


if __name__ == '__main__':
    unittest.main()
