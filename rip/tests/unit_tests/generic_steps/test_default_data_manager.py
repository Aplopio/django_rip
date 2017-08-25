import unittest

from mock import MagicMock

from rip.generic_steps import error_types
from rip.generic_steps.default_data_manager import \
    DefaultDataManager
from rip.generic_steps.error_types import ObjectNotFound, \
    MultipleObjectsFound
from rip.response import Response


class DummyDataManager(DefaultDataManager):
    detail_property_name = 'asdf'


class TestEntityActionsReadDetail(unittest.TestCase):
    def test_should_call_entity_getter(self):
        request = MagicMock()
        request.context_params = dict(request_filters={'id': 1})
        data_manager = DummyDataManager(resource=MagicMock())
        data_manager.get_entity = MagicMock()
        data_manager.get_entity.return_value = expected_obj = object()

        expected_request = data_manager.read_detail(request=request)

        self.assertEqual(expected_request.context_params['asdf'], expected_obj)
        data_manager.get_entity.assert_called_once_with(request, id=1)

    def test_should_apply_request_filters(self):
        request = MagicMock()
        request.context_params = dict(request_filters={'id': 1})

        data_manager = DefaultDataManager(MagicMock())
        data_manager.get_entity = MagicMock()
        data_manager.get_entity.return_value = expected_obj = object()

        expected_request = data_manager.read_detail(request=request)

        self.assertEqual(expected_request.context_params['entity'],
                         expected_obj)
        data_manager.get_entity.assert_called_once_with(request, id=1)


    def test_should_return_response_for_no_object_found(self):
        request = MagicMock()
        request.request_params = {'id': 1}

        data_manager = DefaultDataManager(MagicMock())
        data_manager.get_entity = MagicMock()
        data_manager.get_entity.return_value = expected_obj = None

        response = data_manager.read_detail(request=request)

        self.assertIsInstance(response, Response)
        self.assertFalse(response.is_success)
        self.assertEqual(response.reason, ObjectNotFound)


class TestEntityActionsGetEntity(unittest.TestCase):
    def test_should_raise_for_multiple_objects_found(self):
        data_manager = DefaultDataManager(MagicMock())
        data_manager.get_entity_list = MagicMock()
        data_manager.get_entity_list.return_value = [object(), object()]

        self.assertRaises(MultipleObjectsFound, data_manager.get_entity,
                          request=None, id=2)


    def test_should_return_entity(self):
        data_manager = DefaultDataManager(MagicMock())
        data_manager.get_entity_list = MagicMock()
        data_manager.get_entity_list.return_value = expected_objs = [object()]

        entity = data_manager.get_entity(request=None)

        self.assertEqual(entity, expected_objs[0])

    def test_should_return_none(self):
        data_manager = DefaultDataManager(MagicMock())
        data_manager.get_entity_list = MagicMock()
        data_manager.get_entity_list.return_value = []

        entity = data_manager.get_entity(request=None)

        self.assertEqual(entity, None)


class TestEntityActionsReadList(unittest.TestCase):
    def test_should_call_get_entity_list(self):
        request = MagicMock()
        request.request_params = {'id': 1}
        request.context_params = {}
        data_manager = DefaultDataManager(MagicMock())
        data_manager.get_entity_list = MagicMock()
        data_manager.get_entity_list_total_count = MagicMock()
        data_manager.get_entity_list_total_count.return_value = 1
        data_manager.get_entity_list.return_value = \
            expected_list = [MagicMock()]

        return_request = data_manager.read_list(request)

        self.assertEqual(return_request.context_params['entities'],
                         expected_list)


class TestEntityActionsUpdateDetail(unittest.TestCase):
    def test_should_call_update_with_data(self):
        request = MagicMock()
        request.request_params = {'id': 1}
        request.context_params = {'entity': MagicMock(), 'data':{}}
        data_manager = DefaultDataManager(MagicMock())
        update_entity = MagicMock()
        data_manager.update_entity = update_entity
        update_entity.return_value = expected_entity = MagicMock()

        data_manager.update_detail(request)

        self.assertEqual(request.context_params['entity'], expected_entity)

