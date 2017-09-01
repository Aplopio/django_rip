from http_adapter.default_url_generator import CachedUrlReverser
from http_adapter.url_types import UrlTypes
from rip.schema_fields.field_types import FieldTypes
from rip.schema_fields.string_field import StringField


class ResourceUriField(StringField):
    """
    URI of a resource.
    """
    def __init__(self, resource_name=None, entity_attribute=None,
                 url_type=UrlTypes.detail_url, field_type=FieldTypes.READONLY,
                 required=False, nullable=False, show_in_list=True,
                 max_length=1024, url_reverser_cls=CachedUrlReverser):
        """
        :param resource_name: Name of a Resource Class that has been
        registered with a router
        :param entity_attribute: list of attributes that will be used to
            construct the url. Defaults to ['id']
        """
        super(ResourceUriField, self).__init__(
            max_length=max_length, required=required,
            field_type=field_type, nullable=nullable, show_in_list=show_in_list,
            entity_attribute=entity_attribute or ['id'],)
        self.url_reverser_cls = url_reverser_cls
        self.url_type = url_type
        self.resource_name = resource_name

    def serialize(self, request, value):
        # resource_cls is set by the meta class of the resource
        if self.nullable and value is None:
            return
        resource_name = self.resource_name or \
                        self.resource_cls.get_meta().resource_name
        url_reverser = self.url_reverser_cls(
            resource_name, self.url_type)
        return url_reverser.reverse_to_url(value)

    def clean(self, request, value):
        if value is None:
            return value
        id_index = -2 if value.endswith('/') else -1
        return value.split('/')[id_index]


class ResourceLinkField(ResourceUriField):
    def __init__(self, resource_name, entity_attribute=None,
                 url_type=UrlTypes.detail_url, field_type=FieldTypes.DEFAULT,
                 required=False, nullable=True, show_in_list=True,
                 max_length=1024, url_reverser_cls=CachedUrlReverser):
        super(ResourceLinkField, self).__init__(
            resource_name=resource_name, entity_attribute=entity_attribute,
            url_type=url_type, url_reverser_cls=url_reverser_cls,
            max_length=max_length, required=required,
            field_type=field_type, nullable=nullable, show_in_list=show_in_list)
