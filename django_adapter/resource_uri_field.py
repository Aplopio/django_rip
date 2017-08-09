from django_adapter.default_url_generator import UrlTypes
from rip.schema.base_field import FieldTypes
from rip.schema.string_field import StringField
from django.urls import reverse


class ResourceUriField(StringField):
    """
    URI of a resource.
    """
    def __init__(self, resource_name=None, entity_attribute=None,
                 url_type=UrlTypes.detail_url,
                 field_type=FieldTypes.READONLY,
                 required=False, nullable=False):
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

    def serialize(self, request, value):
        # url reverse can be an expensive operation in large projects.
        # todo: Find a way to cache the results
        url_name = '{}-{}'.format(self.resource_name, self.url_type)
        value = value if isinstance(value, list) else [value]
        return reverse(url_name, args=value)

    def clean(self, request, value):
        if value is None:
            return value
        id_index = -2 if value.endswith('/') else -1
        return value.split('/')[id_index]
