import unittest
from tests.integration_tests.person_resource import PersonDataManager, \
    FriendDataManager, CompanyDataManager


class PersonResourceBaseTestCase(unittest.TestCase):
    def setUp(self):
        """
        Sets the methods of of all entity actions to MagicMocks
        :return:
        """
        PersonDataManager.set_mocks()
        FriendDataManager.set_mocks()
        CompanyDataManager.set_mocks()
