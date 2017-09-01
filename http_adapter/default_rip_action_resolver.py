from http_adapter.url_types import UrlTypes
from rip.crud.crud_actions import CrudActions

method_to_action_mapping = {
    'GET': 'read',
    'POST': 'create',
    'PATCH': 'update',
    'DELETE': 'delete',
    'PUT': 'create_or_update'
}


class DefaultRipActionResolver(object):
    def __init__(self, http_request, url_type, url_kwargs,
                 resource_detail_identifier='id'):
        self.resource_detail_identifier = resource_detail_identifier
        self.url_kwargs = url_kwargs
        self.url_type = url_type
        self.http_request = http_request

    def is_detail_action(self):
        if self.http_request.method == 'POST' and \
                self.url_type == UrlTypes.list_url:
            return True
        return self.resource_detail_identifier in self.url_kwargs and \
            self.url_type == UrlTypes.detail_url

    def determine_end_point(self):
        """
        returns detail, list or aggregates
        """
        if self.is_detail_action():
            return 'detail'
        elif self.url_type == UrlTypes.list_url and \
                self.http_request.method == 'GET':
            return 'list'
        else:
            return None

    def get_action_name(self):
        if self.url_type == UrlTypes.aggregates_url and \
                self.http_request.method == 'GET':
            return CrudActions.GET_AGGREGATES

        endpoint = self.determine_end_point()
        if endpoint is None or \
                method_to_action_mapping.get(self.http_request.method) is None:
            return None
        action_name = "%s_%s" % (
            method_to_action_mapping.get(self.http_request.method), endpoint)
        return action_name
