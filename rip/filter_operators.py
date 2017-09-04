
EQUALS = 'equals'
GT = 'gt'
LT = 'lt'
IN = 'in'

OPERATOR_SEPARATOR = '__'
REVERSE_ORDER = '-'

ALL_OPERATORS = {EQUALS: 1, GT: 1, LT: 1, IN: 1}


def split_to_field_and_filter_type(filter_name):
    filter_split = filter_name.split(OPERATOR_SEPARATOR)
    filter_type = filter_split[-1] if len(filter_split) > 0 else None

    if filter_type in ALL_OPERATORS:
        return OPERATOR_SEPARATOR.join(filter_split[:-1]), filter_type
    else:
        return filter_name, None


def split_to_field_and_order_type(field_name_with_operator):
    if field_name_with_operator.startswith(REVERSE_ORDER):
        return field_name_with_operator[1:], REVERSE_ORDER
    else:
        return field_name_with_operator, None


def transform_to_list(val):
    if isinstance(val, (list, tuple)):
        return val
    else:
        return [val]