from rip.schema.base_field import FieldTypes
from rip.schema.string_field import StringField
from rip import url_constructor


class ResourceUriField(StringField):
    """This field is to be used to add a resource
    with respect to parent resource.

    URI of the resource in context is appended to that of parent.
    """
    def __init__(self, of_type=None, entity_attribute='id',
                 field_type=FieldTypes.READONLY,
                 required=False,
                 nullable=False):
        super(ResourceUriField, self).__init__(
            max_length=1024,
            required=required,
            field_type=field_type,
            nullable=nullable,
            entity_attribute=entity_attribute)
        self.of_type = of_type

    def _get_url_parts(self, entity_name, value, parent_bread_crumbs):
        all_bread_crumbs = parent_bread_crumbs[:]
        all_bread_crumbs.append([entity_name, value])
        return reduce(lambda url_parts,
                             resource_tuple: url_parts + [unicode(val)
                                                          for val
                                                          in resource_tuple],
                      all_bread_crumbs, [])

    def serialize(self, request, value):
        schema = self.of_type or self.schema_cls
        schema_name = schema._meta.schema_name

        return url_constructor.construct_url(
            api_name=request.context_params['api_name'],
            api_version=request.context_params['api_version'],
            schema_name=schema_name,
            entity_id=value,
            parents=request.context_params.get('api_breadcrumbs', [])
        )

    def clean(self, request, value):
        if value is None:
            return value
        id_index = -2 if value.endswith('/') else -1
        return value.split('/')[id_index]
