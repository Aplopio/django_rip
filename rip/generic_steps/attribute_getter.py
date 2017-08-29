
def _get_from_dict(obj, field_name):
    try:
        return obj[field_name]
    except (KeyError, TypeError):
        raise AttributeError(u'{} not in {}'.format(
            field_name, obj))


def _get_from_object(obj, field_name):
    return getattr(obj, field_name)


class DefaultEntityAttributeManager(object):
    def __init__(self, entity):
        self.entity = entity

    def _get_from_dict_or_object(self, field):
        splits = field.split(".")
        val = self.entity
        for split in splits:
            if isinstance(val, dict):
                val = _get_from_dict(val, split)
            else:
                val = _get_from_object(val, split)
        assert val != self.entity
        return val

    def get_attribute(self, field_name):
        if isinstance(field_name, list):
            return [self._get_from_dict_or_object(f)
                    for f in field_name]
        else:
            return self._get_from_dict_or_object(field_name)

    def set_attribute(self, field_name, field_value):
        """
        todo: Add support for setting a.b kind of field_names
        """
        if isinstance(self.entity, dict):
            self.entity[field_name] = field_value
        else:
            setattr(self.entity, field_name, field_value)
