import unittest

from mock import MagicMock

from rip.error_types import ObjectNotFound, \
    MultipleObjectsFound
from rip.generic_steps.default_entity_actions import \
    DefaultEntityActions
from rip.response import Response


class DummyEntityActions(DefaultEntityActions):
    detail_property_name = 'asdf'


class TestEntityActionsReadDetail(unittest.TestCase):
    def test_should_call_entity_getter(self):
        request = MagicMock()
        request.context_params = dict(request_filters={'id': 1})
        entity_actions = DummyEntityActions(schema_cls=None, default_offset=0,
                                            default_limit=20)
        entity_actions.get_entity = MagicMock()
        entity_actions.get_entity.return_value = expected_obj = object()

        expected_request = entity_actions.read_detail(request=request)

        self.assertEqual(expected_request.context_params['asdf'], expected_obj)
        entity_actions.get_entity.assert_called_once_with(request, id=1)

    def test_should_apply_request_filters(self):
        request = MagicMock()
        request.context_params = dict(request_filters={'id': 1})

        entity_actions = DefaultEntityActions(schema_cls=None,
                                              default_offset=0,
                                              default_limit=20)
        entity_actions.get_entity = MagicMock()
        entity_actions.get_entity.return_value = expected_obj = object()

        expected_request = entity_actions.read_detail(request=request)

        self.assertEqual(expected_request.context_params['entity'],
                         expected_obj)
        entity_actions.get_entity.assert_called_once_with(request, id=1)


    def test_should_return_response_for_no_object_found(self):
        request = MagicMock()
        request.request_params = {'id': 1}

        entity_actions = DefaultEntityActions(schema_cls=None,
                                              default_offset=0,
                                              default_limit=20)
        entity_actions.get_entity = MagicMock()
        entity_actions.get_entity.return_value = expected_obj = None

        response = entity_actions.read_detail(request=request)

        self.assertIsInstance(response, Response)
        self.assertFalse(response.is_success)
        self.assertEqual(response.reason, ObjectNotFound)


class TestEntityActionsGetEntity(unittest.TestCase):
    def test_should_raise_for_multiple_objects_found(self):
        entity_actions = DefaultEntityActions(schema_cls=None,
                                              default_offset=0,
                                              default_limit=20)
        entity_actions.get_entity_list = MagicMock()
        entity_actions.get_entity_list.return_value = [object(), object()]

        self.assertRaises(MultipleObjectsFound, entity_actions.get_entity,
                          request=None, id=2)


    def test_should_return_entity(self):
        entity_actions = DefaultEntityActions(schema_cls=None,
                                              default_offset=0,
                                              default_limit=20)
        entity_actions.get_entity_list = MagicMock()
        entity_actions.get_entity_list.return_value = expected_objs = [object()]

        entity = entity_actions.get_entity(request=None)

        self.assertEqual(entity, expected_objs[0])


    def test_should_return_none(self):
        entity_actions = DefaultEntityActions(schema_cls=None,
                                              default_offset=0,
                                              default_limit=20)
        entity_actions.get_entity_list = MagicMock()
        entity_actions.get_entity_list.return_value = []

        entity = entity_actions.get_entity(request=None)

        self.assertEqual(entity, None)


class TestEntityActionsReadList(unittest.TestCase):
    def test_should_call_get_entity_list(self):
        request = MagicMock()
        request.request_params = {'id': 1}
        request.context_params = {}
        entity_actions = DefaultEntityActions(schema_cls=MagicMock(),
                                              default_offset=0,
                                              default_limit=20)
        entity_actions.get_entity_list = MagicMock()
        entity_actions.get_entity_list_total_count = MagicMock()
        entity_actions.get_entity_list_total_count.return_value = 1
        entity_actions.get_entity_list.return_value = \
            expected_list = [MagicMock()]

        return_request = entity_actions.read_list(request)

        self.assertEqual(return_request.context_params['entities'],
                         expected_list)


class TestEntityActionsUpdateDetail(unittest.TestCase):
    def test_should_call_update_with_data(self):
        request = MagicMock()
        request.request_params = {'id': 1}
        request.context_params = {'entity': MagicMock(), 'data':{}}
        entity_actions = DefaultEntityActions(schema_cls=MagicMock(),
                                              default_offset=0,
                                              default_limit=20)
        update_entity = MagicMock()
        entity_actions.update_entity = update_entity
        update_entity.return_value = expected_entity = MagicMock()

        entity_actions.update_detail(request)

        self.assertEqual(request.context_params['entity'], expected_entity)



