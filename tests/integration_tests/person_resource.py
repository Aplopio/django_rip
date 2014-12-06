import mock

from rip.api_schema import ApiSchema
from rip.crud.crud_actions import CrudActions
from rip.crud.crud_resource import CrudResource
from rip.filter_operators import EQUALS
from rip.generic_steps.default_authorization import \
    DefaultAuthorization
from rip.generic_steps.default_entity_actions import \
    DefaultEntityActions
from rip.schema.base_field import FieldTypes
from rip.schema.list_field import ListField
from rip.schema.string_field import StringField
from rip.schema.email_field import EmailField
from rip.schema.integer_field import IntegerField
from rip.schema.list_sub_resource_field import \
    ListSubResourceField
from rip.schema.resource_uri_field import \
    ResourceUriField
from rip.schema.schema_field import SchemaField
from rip.schema.sub_resource_field import \
    SubResourceField


class PersonEntity(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class AddressSchema(ApiSchema):
    city = StringField(max_length=20, field_type=FieldTypes.READONLY)
    country = StringField(max_length=20)

    class Meta:
        schema_name = 'Person_Address'


class CompanySchema(ApiSchema):
    name = StringField(max_length=100)
    registration_number = IntegerField()
    resource_uri = ResourceUriField(entity_attribute='name')

    class Meta:
        schema_name = 'companies'


class FriendSchema(ApiSchema):
    name = StringField(max_length=100)
    relationship_type = StringField(max_length=10)
    resource_uri = ResourceUriField(entity_attribute='name')

    class Meta:
        schema_name = 'friends'


class PersonEntityActions(DefaultEntityActions):
    get_entity_list = mock.MagicMock()
    get_entity_list_total_count = mock.MagicMock()
    get_entity_aggregates = mock.MagicMock()
    update_entity = mock.MagicMock()
    create_entity = mock.MagicMock()
    delete_entity = mock.MagicMock()


class CompanyEntityActions(DefaultEntityActions):
    get_entity_list = mock.MagicMock()
    get_entity_list_total_count = mock.MagicMock()
    update_entity = mock.MagicMock()


class FriendEntityActions(DefaultEntityActions):
    get_entity_list = mock.MagicMock()
    update_entity = mock.MagicMock()
    get_entity_list_total_count = mock.MagicMock()


class CompanyResource(CrudResource):
    filter_by_fields = {'name': (EQUALS), 'person_name': (EQUALS)}
    schema_cls = CompanySchema
    allowed_actions = [CrudActions.READ_LIST,
                       CrudActions.READ_DETAIL,
                       CrudActions.UPDATE_DETAIL]
    entity_actions_cls = CompanyEntityActions
    authorization_cls = DefaultAuthorization


class FriendResource(CrudResource):
    filter_by_fields = {'friend_name': (EQUALS)}
    schema_cls = FriendSchema
    allowed_actions = [CrudActions.READ_LIST,
                       CrudActions.READ_DETAIL,
                       CrudActions.UPDATE_DETAIL]
    entity_actions_cls = FriendEntityActions


class PersonSchema(ApiSchema):
    name = StringField(max_length=100, required=True,
                       nullable=False)
    email = EmailField(max_length=100, nullable=True)
    phone = StringField(max_length=10, field_type=FieldTypes.READONLY)
    address = SchemaField(of_type=AddressSchema, nullable=True)
    company = SubResourceField(resource_cls=CompanyResource,
                               entity_attribute='name',
                               related_filter='person_name',
                               show_in_list=False)
    friends = ListSubResourceField(resource_cls=FriendResource,
                                   entity_attribute='name',
                                   related_filter='friend_name',
                                   show_in_list=False)
    nick_names = ListField(field=StringField())

    class Meta:
        schema_name = 'persons'


class PersonResource(CrudResource):
    filter_by_fields = {'name': (EQUALS), 'nick_names': EQUALS}
    order_by_fields = ['name']
    aggregate_by_fields = ['name']
    schema_cls = PersonSchema
    allowed_actions = [CrudActions.READ_LIST,
                       CrudActions.READ_DETAIL,
                       CrudActions.UPDATE_DETAIL,
                       CrudActions.CREATE_DETAIL,
                       CrudActions.DELETE_DETAIL,
                       CrudActions.GET_AGGREGATES]
    entity_actions_cls = PersonEntityActions
