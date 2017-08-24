import unittest

from mock import MagicMock

from rip.crud.crud_actions import CrudActions
from rip.crud.crud_resource import CrudResource
from rip.crud.pipeline_composer import PipelineComposer
from rip.generic_steps import filter_operators
from rip.request import Request
from rip.schema_fields.boolean_field import BooleanField
from rip.schema_fields.string_field import StringField


class TestCrudResourceOverrides(unittest.TestCase):
    def setUp(self):
        self.pipeline1 = MagicMock(spec=PipelineComposer)
        self.pipeline2 = MagicMock(spec=PipelineComposer)

        class TestResource(CrudResource):
            name = StringField(max_length=32)
            boolean = BooleanField()

            class Meta:
                filter_by_fields = {'name': (filter_operators.EQUALS,)}
                aggregate_by_fields = ('boolean',)
                allowed_actions = [
                    CrudActions.READ_LIST, CrudActions.READ_DETAIL,
                    CrudActions.UPDATE_DETAIL, CrudActions.DELETE_DETAIL,
                    CrudActions.CREATE_DETAIL, CrudActions.CREATE_OR_UPDATE_DETAIL,
                    CrudActions.GET_AGGREGATES
                ]

        self.TestResource = TestResource

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
