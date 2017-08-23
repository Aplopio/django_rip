# -*- coding: utf-8 -*-

from http_adapter.django_crud_resource import DjangoResource
from rip.crud.crud_actions import CrudActions
from rip.generic_steps.default_entity_actions import DefaultEntityActions
from rip.schema.api_schema import ApiSchema
from rip.schema.string_field import StringField


class BlankTestSchema(ApiSchema):
    name = StringField(blank=False)


class BlankTestResource(DjangoResource):
    schema_cls = BlankTestSchema
    allowed_actions = [
        CrudActions.READ_LIST,
        CrudActions.READ_DETAIL,
        CrudActions.CREATE_OR_UPDATE_DETAIL,
        CrudActions.CREATE_DETAIL,
    ]
    entity_actions_cls = DefaultEntityActions
