from http_adapter.default_url_generator import DefaultUrlReverser
from http_adapter.url_types import UrlTypes
from rip.schema.base_field import FieldTypes
from rip.schema.string_field import StringField


class ResourceUriField(StringField):
    """
    URI of a resource.
    """
    def __init__(self, resource_name=None, entity_attribute=None,
                 url_type=UrlTypes.detail_url,
                 field_type=FieldTypes.READONLY,
                 required=False, nullable=False,
                 url_reverser_cls=DefaultUrlReverser):
        """
        :param resource_name: Name of a Resource Class that has been
        registered with a router
        :param entity_attribute: list of attributes that will be used to
            construct the url. Defaults to ['id']
        """
        super(ResourceUriField, self).__init__(
            max_length=1024, required=required,
            field_type=field_type, nullable=nullable,
            entity_attribute=entity_attribute or ['id'])
        self.url_type = url_type
        self.resource_name = resource_name
        self.url_reverser = url_reverser_cls(resource_name, url_type)

    def serialize(self, request, value):
        return self.url_reverser.reverse_to_url(value)

    def clean(self, request, value):
        if value is None:
            return value
        id_index = -2 if value.endswith('/') else -1
        return value.split('/')[id_index]
