import unittest

from rip.generic_steps.default_schema_serializer import \
    DefaultEntitySerializer
from rip.request import Request
from rip.schema.api_schema import ApiSchema
from rip.schema.boolean_field import \
    BooleanField
from rip.schema.string_field import StringField


__all__ = ["TestSerializeSchemaToResponse"]


class TestSerializeSchemaToResponse(unittest.TestCase):
    def setUp(self):
        class TestSchema(ApiSchema):
            id = StringField(required=True)
            name = StringField(max_length=32)
            is_active = BooleanField()

            class Meta:
                schema_name = 'asdf'

        self.TestSchema = TestSchema
        self.serializer = DefaultEntitySerializer(schema_cls=TestSchema)

    def test_should_serialize_to_response(self):
        request = Request(user=None, request_params=None)
        request.context_params['entity'] = dict(id='aaaa', name='asdf', is_active=True)

        request = self.serializer.serialize_detail(request)
        self.assertEqual(request.context_params['serialized_data'],
                         dict(id='aaaa', name='asdf', is_active=True))

    def test_should_not_throw_error_on_missing_non_required_fields(self):
        request = Request(user=None, request_params=None)
        request.context_params['entity'] = dict(id='aaaa', is_active=True)

        request = self.serializer.serialize_detail(request)
        self.assertEqual(request.context_params['serialized_data'],
                         dict(id='aaaa', is_active=True))

    def test_should_throw_error_on_missing_required_fields(self):
        request = Request(user=None, request_params=None)
        request.context_params['entity'] = dict(name='asdf', is_active=True)

        self.assertRaises(AttributeError,
                          self.serializer.serialize_detail, request)

    def test_should_serialize_list_to_response(self):
        request = Request(user=None, request_params=None, context_params={})
        request.context_params['total_count'] = 10
        request.context_params['request_filters'] = {'offset': 0, 'limit': 20}
        request.context_params['entities'] = \
            [dict(id='aaaa', name='asdf', is_active=True),
             dict(id='bbbb', name='asdf', is_active=False)]

        request = self.serializer.serialize_list(request)

        data = request.context_params['serialized_data']['objects']
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0],
                         dict(id='aaaa', name='asdf', is_active=True))
        self.assertEqual(data[1],
                         dict(id='bbbb', name='asdf', is_active=False))
