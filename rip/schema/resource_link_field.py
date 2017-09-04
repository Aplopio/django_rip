from rip.schema.base_field import FieldTypes
from rip.schema.string_field import StringField
from rip import url_constructor


class ResourceLinkField(StringField):
    """This field is to be used to add independent resource.

    URI generated for this field is only for the resource in context
    and not related to parent resource.
    """
    def __init__(self, of_type, entity_attribute='id',
                 field_type=FieldTypes.READONLY,
                 required=False,
                 nullable=False):
        """Constructor for `ResourceLinkField`.

        :param of_type:
            this is schema class for which the field is defined
        :param entity_attribute:
            attribute of the schema defined by `of_type`
            which will be used to generate URI
        :param field_type:
            states the type of the field and
            can take pre-defined `FieldTypes` constants:
            READONLY, DEFAULT, IMMUTABLE, etc.
        :param required:
            ``True`` states this field is required
            when parent resource is created
        :param nullable:
            ``True`` states that this field can take Null values
            while creating/updating the parent resource
        """
        super(ResourceLinkField, self).__init__(
            max_length=1024,
            required=required,
            field_type=field_type,
            nullable=nullable,
            entity_attribute=entity_attribute)
        self.of_type = of_type

    def serialize(self, request, value):
        if value is None:
            return value

        schema = self.of_type
        schema_name = schema._meta.schema_name

        return url_constructor.construct_url(
            api_name=request.context_params['api_name'],
            api_version=request.context_params['api_version'],
            schema_name=schema_name,
            entity_id=value)

    def clean(self, request, value):
        if value is None:
            return value
        id_index = -2 if value.endswith('/') else -1
        url_parts = value.split('/')
        return url_parts[id_index]
