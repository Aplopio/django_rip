import six
from rip.schema.base_field import BaseField, FieldTypes
from rip.schema.sub_resource_field import SubResourceField


class ApiSchemaOptions(object):
    def __init__(self, meta_options, fields, declared_fields):
        if meta_options:
            for override_name in dir(meta_options):
                override = getattr(meta_options, override_name)
                setattr(self, override_name, override)

        self.fields = fields
        self.declared_fields = declared_fields


class ApiSchemaMetaClass(type):
    def __new__(cls, name, bases, attrs):
        fields = {}
        declared_fields = {}

        # Inherit any fields from parent(s).
        try:
            parents = [b for b in bases if issubclass(b, ApiSchema)]
            # Simulate the MRO.
            parents.reverse()

            for p in parents:
                meta_on_parent = getattr(p, '_meta', None)
                fields_declared_on_parent = meta_on_parent.fields if meta_on_parent else {}

                for field_name, field in fields_declared_on_parent.items():
                    fields[field_name] = field
        except NameError:
            pass

        for field_name, field in attrs.copy().items():
            # Runs only once during class construction.
            # Copy should not be a performance hit.
            if isinstance(field, BaseField):
                field = attrs.pop(field_name)
                declared_fields[field_name] = field

        fields.update(declared_fields)
        new_class = super(ApiSchemaMetaClass, cls).__new__(cls, name, bases,
                                                           attrs)

        for field_name, field in fields.items():
            field.schema_cls = new_class

        meta = getattr(new_class, 'Meta', None)
        new_class._meta = ApiSchemaOptions(meta, fields, declared_fields)

        return new_class


class ApiSchema(six.with_metaclass(ApiSchemaMetaClass)):
    def __new__(cls, *args, **kwargs):

        if not hasattr(cls._meta, 'schema_name'):
            raise TypeError(
                'Missing meta property `schema_name` on Schema `{schema_cls}`'
                .format(schema_cls=cls.__name__))

        obj = super(ApiSchema, cls).__new__(cls, *args, **kwargs)
        return obj

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __eq__(self, value):
        for field_name, field_object in self._meta.fields.items():
            if getattr(self, field_name) != getattr(value, field_name):
                return False
        return True

    @classmethod
    def non_readonly_fields(cls):
        return {field_name: field for field_name, field in
                cls._meta.fields.items()
                if field.field_type != FieldTypes.READONLY}

    @classmethod
    def updatable_fields(cls):
        return {field_name: field for field_name, field in
                cls._meta.fields.items()
                if field.field_type == FieldTypes.DEFAULT}

    @classmethod
    def sub_resource_fields(cls):
        return {field_name: field for field_name, field in
                cls._meta.fields.items()
                if isinstance(field, SubResourceField)}

    @classmethod
    def list_fields(cls):
        return {field_name: field for field_name, field in
                cls._meta.fields.items()
                if field.show_in_list}
