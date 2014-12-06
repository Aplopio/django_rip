
class DefaultPostActionHooks(object):

    def __init__(self, schema_cls):
        self.schema_cls = schema_cls

    def read_list_hook(self, request):
        return request

    def read_detail_hook(self, request):
        return request

    def create_detail_hook(self, request):
        return request

    def update_detail_hook(self, request):
        return request

    def delete_detail_hook(self, request):
        return request

    def get_aggregates_hook(self, request):
        return request
