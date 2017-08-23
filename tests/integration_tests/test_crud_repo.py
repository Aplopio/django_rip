from django.test import TestCase
from django.contrib.auth.models import User
from model_adapter.crud_repo import CrudRepo

"""
class TestModelEntityActions(TestCase):
    def setUp(self):
        super(TestModelEntityActions, self).setUp()
        p1 = User.objects.create(username='p1')
        p2 = User.objects.create(username='p2')
        p3 = User.objects.create(username='p3')

        self.crud_repo = CrudRepo(model_cls=User)

    def test_get_list(self):
        assert len(self.crud_repo.get_list(offset=0, limit=10)) == 3

"""