from django_adapter.default_url_generator import UrlTypes
from rip.crud.crud_actions import CrudActions

method_to_action_mapping = {
    'GET': 'read',
    'POST': 'create',
    'PATCH': 'update',
    'DELETE': 'delete',
    'PUT': 'create_or_update'
}


def is_detail_action(http_request, url_type, url_kwargs):
    if http_request.method == 'POST' and url_type == UrlTypes.list_url:
        return True
    return 'id' in url_kwargs


def determine_end_point(http_request, url_type, url_kwargs):
    """
    returns detail, list or aggregates
    """
    if is_detail_action(http_request, url_type, url_kwargs):
        return 'detail'
    elif url_type == UrlTypes.list_url and http_request.method == 'GET':
        return 'list'
    else:
        return None


def get_action_name(http_request, url_type, url_kwargs):
    if url_type == UrlTypes.aggregates_url and http_request.method == 'GET':
        return CrudActions.GET_AGGREGATES

    endpoint = determine_end_point(http_request, url_type, url_kwargs)
    if endpoint is None or \
            method_to_action_mapping.get(http_request.method) is None:
        return None
    action_name = "%s_%s" % (
        method_to_action_mapping.get(http_request.method), endpoint)
    return action_name
