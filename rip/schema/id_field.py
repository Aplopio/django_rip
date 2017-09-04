from rip.schema.base_field import FieldTypes
from rip.schema.integer_field import IntegerField


class IdField(IntegerField):
    def __init__(self, entity_attribute='id'):
        super(IdField, self).__init__(field_type=FieldTypes.READONLY,
                                      required=False,
                                      nullable=False,
                                      entity_attribute=entity_attribute
                                      )
