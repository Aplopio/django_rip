import unittest

from mock import MagicMock, patch

from rip.crud.crud_actions import CrudActions
from rip.crud.crud_resource import CrudResource
from rip.crud.pipeline_composer import PipelineComposer
from rip.generic_steps import default_authentication, error_types
from rip.generic_steps.default_entity_actions import \
    DefaultEntityActions
from rip.schema.api_schema import ApiSchema
from rip.schema.boolean_field import \
    BooleanField
from rip.schema.string_field import StringField


class TestCrudResourceConstruction(unittest.TestCase):
    def setUp(self):
        self.pipeline1 = MagicMock(spec=PipelineComposer)
        self.pipeline2 = MagicMock(spec=PipelineComposer)

        class TestSchema(ApiSchema):
            name = StringField(max_length=32)
            boolean = BooleanField()

        class TestResource(CrudResource):
            schema_cls = TestSchema

        self.TestResource = TestResource
        self.schema = TestSchema

    def test_missing_schema_throws(self):
        class TestResource(CrudResource):
            pass

        self.assertRaises(TypeError, TestResource)

    def test_default_properties(self):
        class DefaultTestResource(CrudResource):
            schema_cls = self.schema

        resource = DefaultTestResource()

        assert len(resource.allowed_actions) == 2
        assert isinstance(resource.request_authentication,
                          default_authentication.DefaultAuthentication)
        assert isinstance(resource.entity_actions, DefaultEntityActions)

    def test_read_detail(self):
        request = MagicMock()

        class DefaultTestResource(CrudResource):
            schema_cls = self.schema

        test_resource = DefaultTestResource()
        test_resource.pipelines[CrudActions.READ_DETAIL] = \
            pipeline = MagicMock()
        test_resource.run_crud_action(CrudActions.READ_DETAIL, request)

        pipeline.assert_called_once_with(request)

    def test_update_detail(self):
        request = MagicMock()

        class DefaultTestResource(CrudResource):
            schema_cls = self.schema
            allowed_actions = [CrudActions.UPDATE_DETAIL]

        test_resource = DefaultTestResource()
        test_resource.pipelines[CrudActions.UPDATE_DETAIL] = \
            pipeline = MagicMock()
        test_resource.run_crud_action(CrudActions.UPDATE_DETAIL, request)

        pipeline.assert_called_once_with(request)

    def test_create_detail(self):
        request = MagicMock()

        class DefaultTestResource(CrudResource):
            schema_cls = self.schema
            allowed_actions = [CrudActions.CREATE_DETAIL]

        test_resource = DefaultTestResource()
        test_resource.pipelines[CrudActions.CREATE_DETAIL] = \
            pipeline = MagicMock()
        test_resource.run_crud_action(CrudActions.CREATE_DETAIL, request)

        pipeline.assert_called_once_with(request)

    def test_delete_detail(self):
        request = MagicMock()

        class DefaultTestResource(CrudResource):
            schema_cls = self.schema
            allowed_actions = [CrudActions.DELETE_DETAIL]

        test_resource = DefaultTestResource()
        test_resource.pipelines[CrudActions.DELETE_DETAIL] = \
            pipeline = MagicMock()
        test_resource.run_crud_action(CrudActions.DELETE_DETAIL, request)

        pipeline.assert_called_once_with(request)

    def test_create_or_update_detail(self):
        expected_response = MagicMock()
        request = MagicMock()

        class DefaultTestResource(CrudResource):
            schema_cls = self.schema
            authentication_cls = MagicMock()
            allowed_actions = [CrudActions.CREATE_OR_UPDATE_DETAIL]

        test_resource = DefaultTestResource()
        test_resource.pipelines[CrudActions.CREATE_OR_UPDATE_DETAIL] = \
            pipeline = MagicMock()
        pipeline.return_value = expected_response

        response = test_resource.run_crud_action(
            CrudActions.CREATE_OR_UPDATE_DETAIL, request)

        assert response == expected_response
        pipeline.assert_called_once_with(request)


class TestMethodNotAllowed(unittest.TestCase):
    def setUp(self):
        class TestResource(CrudResource):
            schema_cls = MagicMock()
            allowed_actions = ()

        self.test_resource = TestResource()

    def assert_forbidden_response(self, response):
        assert not response.is_success
        assert response.reason == error_types.MethodNotAllowed

    def test_forbidden_response_if_methods_not_allowed(self):
        request = MagicMock()
        for action in [CrudActions.READ_DETAIL, CrudActions.READ_LIST,
                       CrudActions.GET_AGGREGATES, CrudActions.CREATE_DETAIL,
                       CrudActions.UPDATE_DETAIL, CrudActions.DELETE_DETAIL,
                       CrudActions.CREATE_OR_UPDATE_DETAIL]:
            response = self.test_resource.run_crud_action(
                action, request=request)
            self.assert_forbidden_response(response)
