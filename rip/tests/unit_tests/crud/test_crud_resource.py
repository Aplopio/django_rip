import unittest

from mock import MagicMock, patch

from rip.crud.crud_actions import CrudActions
from rip.crud.crud_resource import CrudResource
from rip.crud.pipeline_composer import PipelineComposer
from rip.generic_steps import default_authentication, error_types, \
    filter_operators
from rip.generic_steps.default_entity_actions import \
    DefaultEntityActions
from rip.request import Request
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


class TestCrudResourceOverrides(unittest.TestCase):
    def setUp(self):
        self.pipeline1 = MagicMock(spec=PipelineComposer)
        self.pipeline2 = MagicMock(spec=PipelineComposer)

        class TestSchema(ApiSchema):
            name = StringField(max_length=32)
            boolean = BooleanField()

        class TestResource(CrudResource):
            schema_cls = TestSchema
            filter_by_fields = {'name': (filter_operators.EQUALS,)}
            aggregate_by_fields = ('boolean',)
            allowed_actions = [
                CrudActions.READ_LIST, CrudActions.READ_DETAIL,
                CrudActions.UPDATE_DETAIL, CrudActions.DELETE_DETAIL,
                CrudActions.CREATE_DETAIL, CrudActions.CREATE_OR_UPDATE_DETAIL,
                CrudActions.GET_AGGREGATES
            ]

        self.TestResource = TestResource
        self.schema = TestSchema

    def test_get_entity_override(self):
        request = Request(user=MagicMock(), request_params={})
        entity = dict(name='asdf', boolean=True)
        self.TestResource.get_entity = lambda s, r: entity
        test_resource = self.TestResource()

        response = test_resource.run_crud_action(CrudActions.READ_DETAIL,
                                                 request)

        assert response.data == entity

    def test_update_entity_overrides(self):
        data = dict(name='asdf', boolean=True)
        request = Request(user=MagicMock(), request_params={},
                          data=data)

        self.TestResource.get_entity = get_entity = MagicMock()
        updated_entity = dict(name='asdf123', boolean=False)
        self.TestResource.update_entity = lambda s, r, e, ** kwargs: updated_entity

        test_resource = self.TestResource()

        response = test_resource.run_crud_action(
            CrudActions.UPDATE_DETAIL, request)

        get_entity.assert_called_once_with(request)
        assert response.data == updated_entity

    def test_get_list_override(self):
        request = Request(user=MagicMock(), request_params={'name': 1})
        entity = dict(name='asdf', boolean=True)
        total = 899
        self.TestResource.get_entity_list = get_list_fn = MagicMock(
            return_value=[entity])
        self.TestResource.get_total_count = get_total_fn = MagicMock(
            return_value=total)
        test_resource = self.TestResource()

        response = test_resource.run_crud_action(CrudActions.READ_LIST, request)

        assert response.is_success
        assert response.data['objects'] == [entity]
        assert response.data['meta']['total'] == total
        get_list_fn.assert_called_once_with(request, limit=20, offset=0, name=1)
        get_total_fn.assert_called_once_with(request, name=1)

    def test_delete_entity_override(self):
        request = Request(user=MagicMock(), request_params={})
        entity = dict(name='asdf', boolean=True)

        self.TestResource.get_entity = lambda s, r: entity
        self.TestResource.delete_entity = delete_entity_fn = MagicMock()
        test_resource = self.TestResource()

        test_resource.run_crud_action(CrudActions.DELETE_DETAIL, request)

        delete_entity_fn.assert_called_once_with(request, entity)

    def test_create_entity_override(self):
        data = dict(name='asdf', boolean=True)
        request = Request(user=MagicMock(), request_params={}, data=data)

        self.TestResource.create_entity = create_entity_fn = MagicMock()
        test_resource = self.TestResource()

        test_resource.run_crud_action(CrudActions.CREATE_DETAIL, request)

        create_entity_fn.assert_called_once_with(request, **data)

    def test_create_update_entity_override(self):
        data = dict(name='asdf', boolean=True)
        request = Request(user=MagicMock(), request_params={},
                          data=data)
        entity = dict(name='asdf3123', boolean=True)

        self.TestResource.get_entity = get_entity = MagicMock(return_value=entity)
        updated_entity = dict(name='asdf123', boolean=False)
        self.TestResource.update_entity = update_entity = \
            MagicMock(return_value=updated_entity)
        test_resource = self.TestResource()

        response = test_resource.run_crud_action(
            CrudActions.CREATE_OR_UPDATE_DETAIL, request)

        get_entity.assert_called_once_with(request)
        assert response.data == updated_entity
        update_entity.assert_called_once_with(request, entity, **data)

    def test_get_aggregates_override(self):
        request = Request(user=MagicMock(),
                          request_params={'aggregate_by': 'boolean', 'name': 1})
        aggregates = [dict(boolean=True, count=2), dict(boolean=False, count=3)]

        self.TestResource.get_aggregates = get_aggregates_fn = \
            MagicMock(return_value=aggregates)
        test_resource = self.TestResource()

        response = test_resource.run_crud_action(
            CrudActions.GET_AGGREGATES, request)

        get_aggregates_fn.assert_called_once_with(
            request, aggregate_by=['boolean'], name=1)
        assert response.data == aggregates
