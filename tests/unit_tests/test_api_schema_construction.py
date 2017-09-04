import unittest

from rip.api_schema import ApiSchema
from rip.schema.boolean_field import \
    BooleanField
from rip.schema.string_field import StringField
from rip.schema.email_field import EmailField


class TestApiSchemaConstruction(unittest.TestCase):
    def setUp(self):
        class TestSchema(ApiSchema):
            email = EmailField(max_length=50)
            char = StringField(required=True, max_length=100)
            boolean = BooleanField()

            class Meta:
                schema_name = 'asdf'

        self.TestSchema = TestSchema

    def test_should_generate_fields_attribute(self):
        TestSchema = self.TestSchema

        self.assertTrue(hasattr(TestSchema._meta, 'fields'))
        self.assertIn('email', TestSchema._meta.fields)
        self.assertIn('char', TestSchema._meta.fields)
        self.assertIn('boolean', TestSchema._meta.fields)

    def test_attributes_should_be_set_on_instance(self):
        test_schema_obj = self.TestSchema(email='a@b.com',
                                          char='asdf',
                                          boolean=True)

        self.assertEqual(test_schema_obj.email, 'a@b.com')
        self.assertEqual(test_schema_obj.char, 'asdf')
        self.assertTrue(test_schema_obj.boolean)

    def test_should_raise_exception_for_missing_name(self):
        class NameLessSchema(ApiSchema):
            email = EmailField(max_length=50)
            char = StringField(required=True, max_length=100)
            boolean = BooleanField()

        self.assertRaises(TypeError, NameLessSchema,
                          email='asdf', char='char', boolean='boolean')

    def test_should_inherit_fields(self):
        class NewSchema(self.TestSchema):
            new_field = EmailField(max_length=20)

        self.assertTrue('new_field' in NewSchema._meta.fields)
        self.assertTrue('new_field' in NewSchema._meta.declared_fields)
