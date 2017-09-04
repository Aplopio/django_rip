class Request(object):
    """
    All actions objects when called create a request object before passing the call to a handler.
    A request object has a requesting_user, params of the call and the caller. Caller is the name of the
    action object making the call
    """

    def __init__(self, user, request_params, data=None, context_params=None,
                 request_headers=None, request_body=None):
        self.user = user or None
        self.request_params = request_params or {}
        self.data = data or {}
        self.context_params = context_params or {}
        self.request_headers = request_headers or {}
        self.request_body = request_body

    def __eq__(self, val):
        return self.user == val.user and \
               self.request_params == val.request_params and \
               self.data == self.data and \
               self.context_params == val.context_params
