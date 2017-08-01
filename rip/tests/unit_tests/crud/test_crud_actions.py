import unittest

from rip.crud.crud_actions import CrudActions


class TestResolveAction(unittest.TestCase):
    def test_should_resolve_read_detail(self):
        assert CrudActions.resolve_action(
            'read_detail') == CrudActions.READ_DETAIL

    def test_should_resolve_read_list(self):
        assert CrudActions.resolve_action(
            'read_list') == CrudActions.READ_LIST

    def test_should_resolve_create_detail(self):
        assert CrudActions.resolve_action(
            'create_detail') == CrudActions.CREATE_DETAIL

    def test_should_resolve_update_detail(self):
        assert CrudActions.resolve_action(
            'update_detail') == CrudActions.UPDATE_DETAIL

    def test_should_resolve_delete_detail(self):
        assert CrudActions.resolve_action(
            'delete_detail') == CrudActions.DELETE_DETAIL

    def test_should_get_aggregates(self):
        assert CrudActions.resolve_action(
            'get_aggregates') == CrudActions.GET_AGGREGATES
