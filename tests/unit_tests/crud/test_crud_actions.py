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


class TestAllActions(unittest.TestCase):
    def test_should_get_all_actions(self):
        all_actions = CrudActions.get_all_actions()

        assert len(all_actions) == 7
        assert CrudActions.READ_DETAIL in all_actions
        assert CrudActions.READ_LIST in all_actions
        assert CrudActions.CREATE_DETAIL in all_actions
        assert CrudActions.UPDATE_DETAIL in all_actions
        assert CrudActions.PUT_DETAIL in all_actions
        assert CrudActions.DELETE_DETAIL in all_actions
        assert CrudActions.GET_AGGREGATES in all_actions
