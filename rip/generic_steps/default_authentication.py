from rip.generic_steps import error_types
from rip.response import Response


def authenticate(request):
    return request if request.user \
        else Response(is_success=False, reason=error_types.AuthenticationFailed)


class DefaultAuthentication(object):
    def __init__(self, schema_cls):
        self.schema_cls = schema_cls

    def authenticate(self, request):
        return request
