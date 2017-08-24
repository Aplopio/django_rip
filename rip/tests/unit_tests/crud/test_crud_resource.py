import unittest

from mock import MagicMock

from rip.crud.crud_actions import CrudActions
from rip.crud.crud_resource import CrudResource
from rip.crud.pipeline_composer import PipelineComposer
from rip.generic_steps import error_types
from rip.request import Request
from rip.schema_fields.boolean_field import BooleanField
from rip.schema_fields.string_field import StringField


class TestCrudResourceConstruction(unittest.TestCase):
    def setUp(self):
        self.pipeline1 = MagicMock(spec=PipelineComposer)
        self.pipeline2 = MagicMock(spec=PipelineComposer)

        class TestResource(CrudResource):
            name = StringField(max_length=32)
            boolean = BooleanField()

        self.TestResource = TestResource

    def test_read_detail(self):
        request = MagicMock()

        test_resource = self.TestResource()
        test_resource.pipelines[CrudActions.READ_DETAIL] = \
            pipeline = MagicMock()
        test_resource.run_crud_action(CrudActions.READ_DETAIL, request)

        pipeline.assert_called_once_with(request)

    def test_update_detail(self):
        request = MagicMock()

        class DefaultTestResource(CrudResource):

            class Meta:
                allowed_actions = [CrudActions.UPDATE_DETAIL]

        test_resource = DefaultTestResource()
        test_resource.pipelines[CrudActions.UPDATE_DETAIL] = \
            pipeline = MagicMock()
        test_resource.run_crud_action(CrudActions.UPDATE_DETAIL, request)

        pipeline.assert_called_once_with(request)

    def test_create_detail(self):
        request = MagicMock()

        class DefaultTestResource(CrudResource):
            class Meta:
                allowed_actions = [CrudActions.CREATE_DETAIL]

        test_resource = DefaultTestResource()
        test_resource.pipelines[CrudActions.CREATE_DETAIL] = \
            pipeline = MagicMock()
        test_resource.run_crud_action(CrudActions.CREATE_DETAIL, request)

        pipeline.assert_called_once_with(request)

    def test_delete_detail(self):
        request = MagicMock()

        class DefaultTestResource(CrudResource):
            class Meta:
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
            class Meta:
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
            class Meta:
                allowed_actions = ()

        self.test_resource = TestResource()

    def assert_forbidden_response(self, response):
        assert not response.is_success
        assert response.reason == error_types.MethodNotAllowed

    def test_forbidden_response_if_methods_not_allowed(self):
        request = Request(user=MagicMock(), request_params={})
        for action in [CrudActions.READ_DETAIL, CrudActions.READ_LIST,
                       CrudActions.GET_AGGREGATES, CrudActions.CREATE_DETAIL,
                       CrudActions.UPDATE_DETAIL, CrudActions.DELETE_DETAIL,
                       CrudActions.CREATE_OR_UPDATE_DETAIL]:

            response = self.test_resource.run_crud_action(
                action, request=request)
            self.assert_forbidden_response(response)
