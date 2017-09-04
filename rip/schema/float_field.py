# -*- coding: utf-8 -*-

from decimal import Decimal
from rip.schema.base_field import BaseField, FieldTypes


class FloatField(BaseField):
    field_type = float

    def __init__(self, required=False, field_type=FieldTypes.DEFAULT,
                 nullable=True, entity_attribute=None, show_in_list=True,
                 precision=2):
        super(FloatField, self).__init__(required, field_type, nullable,
                                         entity_attribute, show_in_list)
        self.precision = precision


    def serialize(self, request, value):
        format = '%.{}f'.format(self.precision)
        return float(format % value)
