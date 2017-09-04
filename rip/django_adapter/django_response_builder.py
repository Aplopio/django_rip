from functools import partial

import simplejson
from django.http import HttpResponseNotFound, HttpResponseForbidden, \
    HttpResponse, HttpResponseBadRequest

from rip import error_types


http_status_code_mapping = dict(
    GET=200,
    PATCH=202,
    POST=201,
    DELETE=204
)


class HttpAuthenticationFailed(HttpResponse):
    status_code = 401


http_response_mapping = {
    error_types.ObjectNotFound: HttpResponseNotFound,
    error_types.ActionForbidden: HttpResponseForbidden,
    error_types.AuthenticationFailed: HttpAuthenticationFailed,
    error_types.InvalidData: HttpResponseBadRequest,
    error_types.MethodNotAllowed: partial(HttpResponse, status=405)
}


def build_http_response(http_request, response):
    if response.is_success:
        return HttpResponse(
            status=http_status_code_mapping[http_request.method],
            content=simplejson.dumps(response.data),
            content_type='application/json')
        # return a successful response
    else:
        response_cls = http_response_mapping[response.reason]
        return response_cls(content=simplejson.dumps(response.data),
                            content_type="application/json")
