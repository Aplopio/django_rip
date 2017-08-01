
def api_breadcrumbs(url, endpoint):
    url_parts = url.split("/")
    url_iterator = iter(url_parts)
    url_items = zip(url_iterator, url_iterator)

    if len(url_parts) % 2 == 0:
        #this is a request with id at the end.
        # We don't want it in parent bread crumbs
        parent_bread_crumbs = url_items[:-1]
    else:
        parent_bread_crumbs = url_items
    return parent_bread_crumbs


def api_breadcrumb_filters(url, endpoint):
    breadcrumb_filters = {}
    url_parts = url.split("/")
    endpoint_parts = endpoint.split("/")

    if len(endpoint_parts) < len(url_parts) and url_parts[-1] != 'aggregates':
        # if id is present in url, need to map this as well
        endpoint_parts.append('{id}')

    for key, value in zip(endpoint_parts, url_parts):
        if key.startswith("{") and key.endswith("}"):
            breadcrumb_filters[key[1:-1]] = value

    return breadcrumb_filters