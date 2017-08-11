"""
creates an api request given a django http request object
"""
import simplejson
from django import conf
from simplejson import JSONDecodeError

from rip.generic_steps import error_types
from rip.request import Request
from rip.response import Response


class DefaultRipRequestBuilder(object):

    def __init__(self, http_request, url_kwargs):
        self.request_body = http_request.read()
        self.url_kwargs = url_kwargs
        self.http_request = http_request

    def _build_request_params(self):
        request_params = {}
        for key in self.http_request.GET:
            value = self.http_request.GET.getlist(key)
            if len(value) == 1:
                value = value[0]
            request_params[key] = value

        request_params.update(self.url_kwargs)
        return request_params

    def _resolve_user(self):
        return self.http_request.user \
            if not self.http_request.user.is_anonymous() \
            else None

    def _build_request_data(self):
        request_body = self.request_body
        request_meta = self.http_request.META
        content_types = request_meta.get('CONTENT_TYPE', '').split(";")
        if request_body and 'application/json' in content_types:
            request_data = simplejson.loads(request_body)
        else:
            request_data = {}
        return request_data

    def build_rip_request_or_response(self):
        try:
            request_data = self._build_request_data()
        except JSONDecodeError:
            return Response(is_success=False, reason=error_types.InvalidData,
                            data={'error_message': 'Invalid JSON data'})

        return Request(
            user=self._resolve_user(),
            request_params=self._build_request_params(),
            context_params={'protocol': 'http',
                            'timezone': conf.settings.TIME_ZONE,
                            },
            data=request_data,
            request_headers=self.http_request.META,
            request_body=self.request_body
        )
