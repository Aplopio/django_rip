import unittest
from tests.integration_tests.person_resource import PersonEntityActions, \
    FriendEntityActions, CompanyEntityActions


class PersonResourceBaseTestCase(unittest.TestCase):
    def setUp(self):
        """
        Sets the methods of of all entity actions to MagicMocks
        :return:
        """
        PersonEntityActions.set_mocks()
        FriendEntityActions.set_mocks()
        CompanyEntityActions.set_mocks()