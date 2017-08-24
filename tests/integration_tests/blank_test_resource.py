# -*- coding: utf-8 -*-

from http_adapter.django_crud_resource import DjangoResource
from rip.crud.crud_actions import CrudActions
from rip.generic_steps.default_data_manager import DefaultDataManager
from rip.schema_fields.string_field import StringField


class BlankTestResource(DjangoResource):
    name = StringField(blank=False)

    class Meta:
        allowed_actions = [
            CrudActions.READ_LIST,
            CrudActions.READ_DETAIL,
            CrudActions.CREATE_OR_UPDATE_DETAIL,
            CrudActions.CREATE_DETAIL,
        ]
        data_manager_cls = DefaultDataManager
