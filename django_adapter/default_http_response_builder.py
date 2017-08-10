from functools import partial

import simplejson
from django.http import HttpResponseNotFound, HttpResponseForbidden, \
    HttpResponse, HttpResponseBadRequest

from rip.generic_steps import error_types


class HttpAuthenticationFailed(HttpResponse):
    status_code = 401


class DefaultHttpResponseBuilder(object):
    def __init__(self, http_request, rip_response):
        self.rip_response = rip_response
        self.http_request = http_request
        self.http_status_code_mapping = dict(
            GET=200,
            PATCH=202,
            POST=201,
            DELETE=204
        )
        self.http_response_mapping = {
            error_types.ObjectNotFound: HttpResponseNotFound,
            error_types.ActionForbidden: HttpResponseForbidden,
            error_types.AuthenticationFailed: HttpAuthenticationFailed,
            error_types.InvalidData: HttpResponseBadRequest,
            error_types.MethodNotAllowed: partial(HttpResponse, status=405)
        }

    def build_http_response(self):
        if rip_response.is_success:
            return HttpResponse(
                status=self.http_status_code_mapping[http_request.method],
                content=simplejson.dumps(rip_response.data),
                content_type='application/json')
            # return a successful response
        else:
            response_cls = self.http_response_mapping[rip_response.reason]
            return response_cls(content=simplejson.dumps(rip_response.data),
                                content_type="application/json")
