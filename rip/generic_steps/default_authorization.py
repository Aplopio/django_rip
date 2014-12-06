
class DefaultAuthorization(object):
    """
    This class defines the interface of how an authorization class
    must be written. All the functions should take a apiv2 request
    as input. Each function must add to the request object and return
    if successful. If authorization fails, then return a response
    with is_success as false and a reason code. It is recommended that you
    use authorization failed reason code. By default all actions are permitted
    for all users
    """

    def __init__(self, schema_cls):
        self.schema_cls = schema_cls

    def add_read_list_filters(self, request):
        """
        This step is called before read_list entity action
        Override this to add request filters to return objects accessible to the
        user.

        :param request:
        :return: request if success, response if unauthorized
        """
        return request


    def authorize_read_detail(self, request):
        """
        :param request:
        :return: request if success, response if unauthorized
        """
        return request

    def authorize_update_detail(self, request):
        """
        :param request:
        :return: request if success, response if unauthorized
        """
        return request

    def authorize_delete_detail(self, request):
        """
        :param request:
        :return: request if success, response if unauthorized
        """
        return request

    def authorize_create_detail(self, request):
        """
        :param request:
        :return: request if success, response if unauthorized
        """
        return request
