def _get_from_dict(entity, field_name):
    try:
        return entity[field_name]
    except (KeyError, TypeError):
        raise AttributeError(u'{} not in {}'.format(field_name, entity))


def _get_from_object(entity, field_name):
    return getattr(entity, field_name)


def _get_from_dict_or_object(entity, field):
    if isinstance(entity, dict):
        return _get_from_dict(entity, field)
    return _get_from_object(entity, field)


def get_attribute(entity, field_name):
    if isinstance(field_name, list):
        return [_get_from_dict_or_object(entity, f) for f in field_name]
    else:
        return _get_from_dict_or_object(entity, field_name)
