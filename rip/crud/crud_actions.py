class CrudActions(object):
    GET_AGGREGATES = 'get_aggregates'
    READ_LIST = 'read_list'
    READ_DETAIL = 'read_detail'
    CREATE_DETAIL = 'create_detail'
    DELETE_DETAIL = 'delete_detail'
    UPDATE_DETAIL = 'update_detail'
    PUT_DETAIL = 'put_detail'
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
            cls.GET_AGGREGATES,
            cls.READ_LIST,
            cls.READ_DETAIL,
            cls.CREATE_DETAIL,
            cls.DELETE_DETAIL,
            cls.UPDATE_DETAIL,
            cls.PUT_DETAIL
        )


def _build_reverse_dictionary(cls):
    return {v: k for k, v in cls.__dict__.items() if
            k != '_reverse_dictionary'}
