
def _get_parent_url_part(parents):
    url = ''
    for parent_name, parent_id in parents:
        url += '{}/{}/'.format(parent_name, parent_id)
    return url


def construct_url(api_name, api_version, schema_name,
                  entity_id, parents=None):

    if parents is not None:
        parent_url_part = _get_parent_url_part(parents)
    else:
        parent_url_part = ''
    link_url = u"/{api_name}/{api_version}/{parent_part}{schema_name}/{entity_id}/".\
    format(api_name=api_name,
           api_version=api_version,
           parent_part=parent_url_part,
           schema_name=schema_name,
           entity_id=entity_id)
    return link_url