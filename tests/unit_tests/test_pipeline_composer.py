import unittest

from mock import MagicMock
from mock import patch as mock_patch

from rip import pipeline_composer
from rip.pipeline_composer import PipelineComposer
from rip.request import Request
from rip.response import Response


class TestPipelineComposer(unittest.TestCase):
    def setUp(self):
        self.get_obj = MagicMock()
        self.del_obj = MagicMock()
        self.get_obj.__name__ = 'get_obj'
        self.del_obj.__name__ = 'del_obj'
        self.get_obj.return_value = Request(user=None, request_params=None)
        self.del_obj.return_value = Response()

    def test_api_method_calls_handler(self):
        test_api_method = PipelineComposer(pipeline=[self.get_obj])
        self.get_obj.return_value = Response()
        expected_request = Request(user=None,
                                   request_params={'somearg1': 1,
                                                   'somearg2': 2})
        test_api_method(expected_request)

        self.get_obj.assert_called_with(request=expected_request)

    def test_api_method_calls_all_functions_in_pipeline(self):
        test_api_method = PipelineComposer(
            pipeline=[self.get_obj, self.del_obj])
        expected_request = Request(user=None,
                                   request_params={'somearg1': 1,
                                                   'somearg2': 2})
        test_api_method(expected_request)

        self.get_obj.assert_called_with(
            request=expected_request)
        self.del_obj.assert_called_with(
            request=expected_request)

    def test_api_method_exits_pipeline_on_response(self):
        test_method = PipelineComposer(pipeline=[self.get_obj, self.del_obj])
        expected_response = Response()
        expected_request = Request(user=None,
                                   request_params={'somearg1': 1,
                                                   'somearg2': 2})
        self.get_obj.return_value = expected_response

        test_method(expected_request)

        self.get_obj.assert_called_with(
            request=expected_request)
        self.assertEqual(self.del_obj.call_count, 0)

    def test_api_method_throws_if_no_response_from_last_handler(self):
        test_method = PipelineComposer(pipeline=[self.get_obj, self.del_obj])
        expected_request = Request(
            user=None, request_params={})
        self.get_obj.return_value = expected_request
        self.del_obj.return_value = expected_request

        self.assertRaises(AssertionError, test_method,
                          request=expected_request)

    def test_api_method_throws_for_non_standard_response(self):
        test_method = PipelineComposer(pipeline=[self.get_obj])
        self.get_obj.return_value = object()
        request = Request(user=None, request_params=None)

        self.assertRaises(AssertionError, test_method, request)


class TestComposePipeline(unittest.TestCase):
    @mock_patch.object(pipeline_composer, 'PipelineComposer')
    def test_compose_pipeline_calls_pipeline_composer(self, PipelineComposer):
        pipeline_composer.compose_pipeline(name='asdf', pipeline=['asdf'])

        PipelineComposer.assertCalledOnceWith(name='asdf', pipeline=['asdf'])
