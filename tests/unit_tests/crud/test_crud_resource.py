import unittest

from hamcrest.core import assert_that
from hamcrest.core.core.isequal import equal_to
from mock import MagicMock, patch

from rip.api_schema import ApiSchema
from rip.crud.crud_resource import CrudResource, CrudActions, \
    crud_pipeline_factory
from rip.generic_steps import default_authentication
from rip.generic_steps.default_entity_actions import \
    DefaultEntityActions
from rip.pipeline_composer import PipelineComposer
from rip.schema.boolean_field import \
    BooleanField
from rip.schema.string_field import StringField
from rip import error_types


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

        assert len(resource.configuration['allowed_actions']) == 2
        assert isinstance(resource.configuration['authentication'],
                          default_authentication.DefaultAuthentication)
        assert isinstance(resource.configuration['entity_actions'],
                          DefaultEntityActions)

    def test_return_response_if_method_is_not_allowed(self):
        custom_auth = MagicMock()
        request = MagicMock()

        class DefaultTestResource(CrudResource):
            schema_cls = self.schema
            authentication_cls = custom_auth
            allowed_actions=[
                    CrudActions.READ_LIST,
                    CrudActions.READ_DETAIL
                ]


        test_resource = DefaultTestResource()
        response = test_resource.delete_detail(request)

        assert_that(response.is_success, equal_to(False))
        assert_that(response.reason, equal_to(error_types.MethodNotAllowed))

    @patch.object(crud_pipeline_factory, 'read_detail_pipeline')
    def test_read_detail(self, mock_create_pipeline):
        custom_auth = MagicMock()
        mock_create_pipeline.return_value = pipeline = MagicMock()
        request = MagicMock()

        class DefaultTestResource(CrudResource):
            schema_cls = self.schema
            authentication_cls = custom_auth

        test_resource = DefaultTestResource()
        test_resource.read_detail(request)

        pipeline.assert_called_once_with(request=request)

    @patch.object(crud_pipeline_factory, 'update_detail_pipeline')
    def test_update_detail(self, mock_create_pipeline):
        custom_auth = MagicMock()
        mock_create_pipeline.return_value = pipeline = MagicMock()
        request = MagicMock()

        class DefaultTestResource(CrudResource):
            schema_cls = self.schema
            authentication_cls = custom_auth
            allowed_actions = [CrudActions.UPDATE_DETAIL]

        test_resource = DefaultTestResource()
        test_resource.update_detail(request)

        pipeline.assert_called_once_with(request=request)

    @patch.object(crud_pipeline_factory, 'create_detail_pipeline')
    def test_create_detail(self, mock_create_pipeline):
        custom_auth = MagicMock()
        mock_create_pipeline.return_value = pipeline = MagicMock()
        request = MagicMock()

        class DefaultTestResource(CrudResource):
            schema_cls = self.schema
            authentication_cls = custom_auth
            allowed_actions = [CrudActions.CREATE_DETAIL]

        test_resource = DefaultTestResource()
        test_resource.create_detail(request)

        pipeline.assert_called_once_with(request=request)

    @patch.object(crud_pipeline_factory, 'delete_detail_pipeline')
    def test_delete_detail(self, mock_delete_pipeline):
        custom_auth = MagicMock()
        mock_delete_pipeline.return_value = pipeline = MagicMock()
        request = MagicMock()

        class DefaultTestResource(CrudResource):
            schema_cls = self.schema
            authentication_cls = custom_auth
            allowed_actions = [CrudActions.DELETE_DETAIL]

        test_resource = DefaultTestResource()
        test_resource.delete_detail(request)

        pipeline.assert_called_once_with(request=request)
