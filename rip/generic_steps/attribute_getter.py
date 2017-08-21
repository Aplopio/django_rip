
class DefaultEntityAttributeManager(object):
    def __init__(self, entity):
        self.entity = entity

    def _get_from_dict(self, field_name):
        try:
            return self.entity[field_name]
        except (KeyError, TypeError):
            raise AttributeError(u'{} not in {}'.format(
                field_name, self.entity))

    def _get_from_object(self, field_name):
        return getattr(self.entity, field_name)

    def _get_from_dict_or_object(self, field):
        if isinstance(self.entity, dict):
            return self._get_from_dict(field)
        return self._get_from_object(field)

    def get_attribute(self, field_name):
        """
        todo: Add support for a.b kind of access for nested access to
        fields in an entity
        """
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
