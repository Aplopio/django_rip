def _get_from_dict(entity, field_name):
    try:
        return entity[field_name]
    except (KeyError, TypeError):
        raise AttributeError(u'{} not in {}'.format(field_name, entity))


def _get_from_object(entity, field_name):
        return getattr(entity, field_name)


def get_attribute(entity, field_name):
    if isinstance(entity, dict):
        return _get_from_dict(entity, field_name)

    return _get_from_object(entity, field_name)
