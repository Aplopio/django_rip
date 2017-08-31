import mock

from http_adapter.django_crud_resource import DjangoResource
from http_adapter.django_router import DefaultRouter
from http_adapter.resource_uri_field import ResourceUriField
from rip.crud import crud_actions
from rip.crud.crud_actions import CrudActions
from rip.crud.crud_resource import CrudResource
from rip.generic_steps.default_data_manager import \
    DefaultDataManager
from rip.generic_steps.filter_operators import EQUALS
from rip.schema_fields.field_types import FieldTypes
from rip.schema_fields.email_field import EmailField
from rip.schema_fields.integer_field import IntegerField
from rip.schema_fields.list_field import ListField
from rip.schema_fields.schema_field import SchemaField
from rip.schema_fields.string_field import StringField


class PersonEntity(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class PersonDataManager(DefaultDataManager):
    @classmethod
    def set_mocks(cls):
        cls.get_entity_list = mock.MagicMock()
        cls.get_entity_list_total_count = mock.MagicMock()
        cls.get_entity_aggregates = mock.MagicMock()
        cls.update_entity = mock.MagicMock()
        cls.create_entity = mock.MagicMock()
        cls.delete_entity = mock.MagicMock()


class CompanyDataManager(DefaultDataManager):
    @classmethod
    def set_mocks(cls):
        cls.get_entity_list = mock.MagicMock()
        cls.get_entity_list_total_count = mock.MagicMock()
        cls.update_entity = mock.MagicMock()


class FriendDataManager(DefaultDataManager):
    @classmethod
    def set_mocks(cls):
        cls.get_entity_list = mock.MagicMock()
        cls.update_entity = mock.MagicMock()
        cls.get_entity_list_total_count = mock.MagicMock()


class CompanyResource(DjangoResource):
    name = StringField(max_length=100)
    registration_number = IntegerField()
    resource_uri = ResourceUriField(entity_attribute='name')

    class Meta:
        filter_by_fields = {'name': (EQUALS,), 'person_name': (EQUALS,)}
        allowed_actions = [CrudActions.READ_LIST,
                           CrudActions.READ_DETAIL,
                           CrudActions.UPDATE_DETAIL]
        data_manager_cls = CompanyDataManager


class FriendResource(DjangoResource):
    name = StringField(max_length=100)
    relationship_type = StringField(max_length=10)
    resource_uri = ResourceUriField(entity_attribute='name')

    class Meta:
        filter_by_fields = {'friend_name': (EQUALS,)}
        allowed_actions = [CrudActions.READ_LIST,
                           CrudActions.READ_DETAIL,
                           CrudActions.UPDATE_DETAIL]
        data_manager_cls = FriendDataManager


class AddressSchema(DjangoResource):
    city = StringField(max_length=20, field_type=FieldTypes.READONLY)
    country = StringField(max_length=20)


class PersonResource(DjangoResource):
    name = StringField(max_length=100, required=True,
                       nullable=False, blank=False)
    email = EmailField(max_length=100, nullable=True)
    phone = StringField(max_length=10, field_type=FieldTypes.READONLY)
    address = SchemaField(of_type=AddressSchema, nullable=True)
    company = StringField(show_in_list=False, nullable=True)
    nick_names = ListField(field=StringField())
    id = StringField(field_type=FieldTypes.IMMUTABLE)

    class Meta:
        resource_name = 'person'
        filter_by_fields = {'name': (EQUALS,), 'nick_names': EQUALS}
        order_by_fields = ['name']
        aggregate_by_fields = ['name']
        allowed_actions = crud_actions.ALL_ACTIONS
        data_manager_cls = PersonDataManager

router = DefaultRouter()
router.register(PersonResource)
