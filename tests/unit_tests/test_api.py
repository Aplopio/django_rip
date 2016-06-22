import unittest

from mock import MagicMock

from rip.api import Api
from rip.api_schema import ApiSchema
from rip.crud.crud_resource import CrudResource
from rip.pipeline_composer import PipelineComposer
from rip.request import Request
from rip.schema.string_field import StringField
from rip.view.view_resource import ViewResource


class TestApi(unittest.TestCase):
    def setUp(self):
        self.http_api = Api(name='api', version='v1')
        self.action1 = MagicMock(spec=PipelineComposer)
        self.action2 = MagicMock(spec=PipelineComposer)

        class TestSchema(ApiSchema):
            name = StringField(max_length=100)

            class Meta:
                schema_name = 'test_objs'

        class TestResource(CrudResource):
            action1 = self.action1
            action2 = self.action2

            schema_cls = TestSchema

        class TestViewResource_1(ViewResource):
            schema_cls = TestSchema

        class TestViewResource_2(ViewResource):
            schema_cls = TestSchema

        self.TestResource = TestResource
        self.TestViewResource_1 = TestViewResource_1
        self.TestViewResource_2 = TestViewResource_2

    def test_registered_crud_resource_should_be_accessible_to_call(self):
        test_resource = self.TestResource()
        # Making an assumption that Resource schema name will be used to
        # access -> Useful for serialization
        self.http_api.register_resource('test_objs', test_resource)
        request = Request(user=None, request_params={})

        resource = self.http_api.resolve_resource('test_objs')
        resource.action1(request=request)

    def test_registered_view_resources_should_be_accessible_to_call(self):
        test_view_resource_1 = self.TestViewResource_1()
        test_view_resource_2 = self.TestViewResource_2()

        self.http_api.register_resource('foo/bar', test_view_resource_1)
        self.http_api.register_resource('boo/car', test_view_resource_2)
        request = Request(user=None, request_params={})

        resource_1 = self.http_api.resolve_resource('foo/bar')
        resource_2 = self.http_api.resolve_resource('boo/car')
        endpoint_1 = self.http_api.resolve_endpoint('foo/bar')
        endpoint_2 = self.http_api.resolve_endpoint('boo/car')

        assert isinstance(resource_1, self.TestViewResource_1)
        assert isinstance(resource_2, self.TestViewResource_2)
        assert endpoint_1 == 'foo/bar'
        assert endpoint_2 == 'boo/car'


    def test_register_with_mismatching_schema_raises(self):
        test_resource = self.TestResource()
        self.assertRaises(ValueError, self.http_api.register_resource,
                          'invalid_name', test_resource)

    def test_registered_action_should_be_accessible_to_call(self):
        pass
