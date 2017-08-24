import six
from rip.schema_fields.base_field import BaseField
from rip.schema_fields.field_types import FieldTypes


class ResourceSchemaOptions(object):
    def __init__(self, meta_options, all_fields, declared_fields):
        if meta_options:
            for override_name in meta_options:
                setattr(self, override_name, meta_options[override_name])
        self.meta_options = {key: val for key, val in meta_options.items()
                             if not key.startswith('__')}
        self._all_fields = all_fields
        self._declared_fields = declared_fields


class ResourceSchemaMetaClass(type):
    def __new__(cls, name, bases, attrs):
        all_fields = {}
        declared_fields = {}
        meta_options = {}

        # Inherit any fields from parent(s).
        try:
            parents = [b for b in bases if issubclass(b, ResourceSchemaMixin)]
            # Simulate the MRO.
            parents.reverse()

            for p in parents:
                # copy the fields from parent
                meta_on_parent = getattr(p, '_meta', None)
                fields_declared_on_parent = meta_on_parent._all_fields \
                    if meta_on_parent else {}

                for field_name, field in fields_declared_on_parent.items():
                    all_fields[field_name] = field

                # copy the meta option definitions from parent
                meta_options_on_parent = meta_on_parent.meta_options \
                    if meta_on_parent else {}
                meta_options.update(meta_options_on_parent)
        except NameError:
            pass

        for field_name, field in attrs.copy().items():
            # Runs only once during class construction.
            # Copy should not be a performance hit.
            if isinstance(field, BaseField):
                field = attrs.pop(field_name)
                declared_fields[field_name] = field

        all_fields.update(declared_fields)
        new_class = super(ResourceSchemaMetaClass, cls).__new__(
            cls, name, bases, attrs)

        for field_name, field in all_fields.items():
            field.resource_cls = new_class

        meta_cls = getattr(new_class, 'Meta', None)

        if meta_cls:
            for override_name in dir(meta_cls):
                override = getattr(meta_cls, override_name)
                meta_options[override_name] = override

        new_class._meta = ResourceSchemaOptions(meta_options, all_fields,
                                                declared_fields)

        return new_class


class ResourceSchemaMixin(six.with_metaclass(ResourceSchemaMetaClass)):

    @classmethod
    def non_readonly_fields(cls):
        return {field_name: field for field_name, field in
                cls.all_fields().items()
                if field.field_type != FieldTypes.READONLY}

    @classmethod
    def updatable_fields(cls):
        return {field_name: field for field_name, field in
                cls.all_fields().items()
                if field.field_type == FieldTypes.DEFAULT}

    @classmethod
    def list_fields(cls):
        return {field_name: field for field_name, field in
                cls.all_fields().items()
                if field.show_in_list}

    @classmethod
    def all_fields(cls):
        return cls._meta._all_fields

    @classmethod
    def get_meta(cls):
        return cls._meta
