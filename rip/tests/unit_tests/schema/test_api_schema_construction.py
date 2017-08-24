import unittest

from mock import MagicMock

from rip.crud.crud_resource import CrudResource
from rip.generic_steps.default_data_manager import DefaultDataManager
from rip.schema_fields.boolean_field import \
    BooleanField
from rip.schema_fields.email_field import EmailField
from rip.schema_fields.integer_field import IntegerField
from rip.schema_fields.string_field import StringField


class TestApiSchemaConstruction(unittest.TestCase):
    def setUp(self):
        class TestSchema(CrudResource):
            email = EmailField(max_length=50)
            char = StringField(required=True, max_length=100)
            boolean = BooleanField()

            class Meta:
                resource_name = 'asdf'

        self.TestSchema = TestSchema

    def test_should_generate_fields_attribute(self):
        TestSchema = self.TestSchema

        self.assertTrue(hasattr(TestSchema._meta, '_all_fields'))
        self.assertIn('email', TestSchema.all_fields())
        self.assertIn('char', TestSchema.all_fields())
        self.assertIn('boolean', TestSchema.all_fields())

    def test_should_inherit_meta_attrs(self):
        new_resource_name = 'something'
        expected_data_manager = MagicMock()

        class NewSchema(self.TestSchema):
            class Meta:
                resource_name = new_resource_name
                data_manager_cls = expected_data_manager

        assert self.TestSchema.get_meta().resource_name == 'asdf'
        assert NewSchema.get_meta().resource_name == new_resource_name

        assert self.TestSchema.get_meta().data_manager_cls == \
               DefaultDataManager
        assert NewSchema.get_meta().data_manager_cls == \
               expected_data_manager

    def test_should_override_meta_attrs(self):
        new_resource_name1 = 'something'
        new_resource_name2 = 'something new'
        expected_data_manager1 = MagicMock()
        expected_data_manager2 = MagicMock()

        class NewSchema(self.TestSchema):
            class Meta:
                resource_name = new_resource_name1
                data_manager_cls = expected_data_manager1

        class NewSchema2(NewSchema):
            class Meta:
                resource_name = new_resource_name2
                data_manager_cls = expected_data_manager2

        assert NewSchema2.get_meta().resource_name == new_resource_name2
        assert NewSchema2.get_meta().data_manager_cls == \
            expected_data_manager2

    def test_should_inherit_fields(self):
        class NewSchema(self.TestSchema):
            new_field = EmailField(max_length=20)

        self.assertTrue('new_field' in NewSchema.all_fields())
        self.assertTrue('new_field' in NewSchema._meta._declared_fields)

    def test_should_override_inherited_fields(self):
        expected_field = StringField(required=True, max_length=100)
        expected_field1 = IntegerField(required=True)

        class NewSchema(self.TestSchema):
            email = expected_field

        class NewSchema2(NewSchema):
            email = expected_field1

        assert NewSchema.all_fields()['email'] == expected_field
        assert NewSchema2.all_fields()['email'] == expected_field1
