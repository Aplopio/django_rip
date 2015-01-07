# -*- coding: utf-8 -*-

from rip.schema.string_field import StringField
from rip.api_schema import ApiSchema
from rip.crud.crud_resource import CrudResource
from rip.crud.crud_actions import CrudActions
from rip.generic_steps.default_entity_actions import DefaultEntityActions


class BlankTestSchema(ApiSchema):
    name = StringField(blank=False)


class BlankTestResource(CrudResource):
    schema_cls = BlankTestSchema
    allowed_actions = [
        CrudActions.READ_LIST,
        CrudActions.READ_DETAIL,
        CrudActions.CREATE_OR_UPDATE_DETAIL,
        CrudActions.CREATE_DETAIL,
    ]
    entity_actions_cls = DefaultEntityActions
