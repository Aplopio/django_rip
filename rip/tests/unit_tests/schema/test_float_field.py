# -*- coding: utf-8 -*-

import unittest
from decimal import Decimal

from rip.schema.float_field import FloatField


class TestFloatField(unittest.TestCase):
    def test_serialize_should_round_off_to_default_precision(self):
        float_field = FloatField()
        assert float_field.serialize(request={}, value=23.45667) == 23.46

    def test_serialize_should_round_off_to_1(self):
        float_field = FloatField(precision=1)
        assert float_field.serialize(request={}, value=23.45667) == 23.5
