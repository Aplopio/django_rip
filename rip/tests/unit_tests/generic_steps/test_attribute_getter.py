import unittest

import collections
from mock import MagicMock

from rip.generic_steps import default_authentication, error_types
from rip.generic_steps.attribute_getter import DefaultEntityAttributeManager
from rip.request import Request

Person = collections.namedtuple('Person', 'name age gender father')


class TestAttributeGetter(unittest.TestCase):
    def setUp(self):
        self.object_entity = Person(
            "Jane", 23, 'Male',
            Person("Jane's Father", 50, 'Male',
                   Person("Jane's Grandpa", 80, 'Male', None)))
        self.dict_entity = {
            'field1': 'asdf',
            'field2': {'deep_field1': '123',
                       'deep_field2': {'deeper_field1': '123123'}},
            'object_field': self.object_entity
        }

    def test_access_to_dict_field(self):
        attribute_getter = DefaultEntityAttributeManager(
            entity=self.dict_entity)
        assert attribute_getter.get_attribute('field1') == 'asdf'

    def test_access_to_object_field(self):
        attribute_getter = DefaultEntityAttributeManager(
            entity=self.object_entity)
        assert attribute_getter.get_attribute('name') == 'Jane'

    def test_access_to_list_field_name(self):
        attribute_getter = DefaultEntityAttributeManager(
            entity=self.object_entity)
        assert attribute_getter.get_attribute(['name', 'age']) == ['Jane', 23]

    def test_access_to_deep_dict_field(self):
        attribute_getter = DefaultEntityAttributeManager(
            entity=self.dict_entity)
        assert attribute_getter.get_attribute('object_field.name') == 'Jane'
        assert attribute_getter.get_attribute(
            'object_field.father.father.name') == "Jane's Grandpa"

    def test_access_to_list_of_deep_fields(self):
        attribute_getter = DefaultEntityAttributeManager(
            entity=self.dict_entity)
        assert attribute_getter.get_attribute('object_field.name') == 'Jane'
        assert attribute_getter.get_attribute(
            ['object_field.father.father.name', 'object_field.father.age']) == \
            ["Jane's Grandpa", 50]
