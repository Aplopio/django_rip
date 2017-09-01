from django.test import TestCase
from mock import patch, MagicMock

from http_adapter.default_rip_request_builder import DefaultRipRequestBuilder
from rip.request import Request
from tests import request_factory
from tests.integration_tests.resources_for_testing import PersonDataManager, \
    FriendDataManager, CompanyDataManager

_sentinel = object()


class EndToEndBaseTestCase(TestCase):
    def setUp(self):
        """
        Sets the methods of of all entity actions to MagicMocks
        :return:
        """
        PersonDataManager.set_mocks()
        FriendDataManager.set_mocks()
        CompanyDataManager.set_mocks()

    def patch_module_function(self, module, fn_name, return_value=_sentinel):
        patcher = patch.object(module, fn_name, autospec=True)
        self.addCleanup(patcher.stop)
        patched_fn = patcher.start()
        patched_fn.return_value = return_value \
            if return_value != _sentinel else MagicMock()
        return patched_fn
