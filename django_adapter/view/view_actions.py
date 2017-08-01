class ViewActions(object):
    READ = 'read'

    _reverse_dictionary = None

    @classmethod
    def _get_reverse_dictionary(cls):
        if not cls._reverse_dictionary:
            cls._reverse_dictionary = _build_reverse_dictionary(cls)
        return cls._reverse_dictionary

    @classmethod
    def resolve_action(cls, name):
        cls_attr = cls._get_reverse_dictionary()[name]
        return getattr(cls, cls_attr)

    @classmethod
    def get_all_actions(cls):
        return (
            cls.READ,
        )


def _build_reverse_dictionary(cls):
    return {v: k for k, v in cls.__dict__.items() if
            k != '_reverse_dictionary'}
