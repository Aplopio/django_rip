method_to_action_mapping = {'GET': 'read',
                            'POST': 'create',
                            'PATCH': 'update',
                            'DELETE': 'delete'}


def is_detail_url(http_request, url):
    if http_request.method == 'POST':
        return True
    return len(url.split('/')) % 2 == 0


def determine_end_point(http_request, url):
    """
    returns detail, list or aggregates
    """
    if url.endswith('aggregates') or url.endswith('aggregates/'):
        return 'aggregates'
    else:
     return 'detail' if is_detail_url(http_request, url) else 'list'

def is_valid_resource(url, api):
    return True if api.resolve_resource(url) else False

def resolve_action(http_request, url, api):
    try:
        resource = api.resolve_resource(url)
        endpoint = determine_end_point(http_request, url)
        if endpoint == 'aggregates':
            resource_action = 'get_aggregates'
        else:
            resource_action = "%s_%s" % (
                method_to_action_mapping.get(http_request.method), endpoint)
        action = getattr(resource, resource_action)
        return action
    except AttributeError:
        return None
