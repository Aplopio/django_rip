def patch_class_field(cls, field_name, value):
    """
    Patches a field on a class with the value
    unpatches it when the method exits
    :param cls:
    :param field_name:
    :param value:
    :return:
    """

    def outer_wrapper(func):
        def wrapper(*args, **kwargs):
            old_field_value = getattr(cls, field_name)
            setattr(cls, field_name, value)
            try:
                return func(*args, **kwargs)
            finally:
                setattr(cls, field_name, old_field_value)

        return wrapper

    return outer_wrapper
