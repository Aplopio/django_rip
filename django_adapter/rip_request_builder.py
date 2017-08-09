"""
creates an api request given a django http request object
"""
import simplejson
from django import conf
from simplejson import JSONDecodeError

from rip.generic_steps import error_types
from rip.request import Request
from rip.response import Response


def _build_request_params(http_request, url_kwargs):
    request_params = {}
    for key in http_request.GET:
        value = http_request.GET.getlist(key)
        if len(value) == 1:
            value = value[0]
        request_params[key] = value

    request_params.update(url_kwargs)
    return request_params


def _resolve_user(http_request):
    return http_request.user \
        if not http_request.user.is_anonymous() \
        else None


def _build_request_data(request_body, request_meta):
    content_types = request_meta.get('CONTENT_TYPE', '').split(";")
    if request_body and 'application/json' in content_types:
        request_data = simplejson.loads(request_body)
    else:
        request_data = {}
    return request_data


def build_rip_request_or_response(http_request, url_kwargs):
    request_body = http_request.read()
    try:
        request_data = _build_request_data(request_body, http_request.META)
    except JSONDecodeError:
        return Response(is_success=False, reason=error_types.InvalidData,
                        data={'error_message': 'Invalid JSON data'})

    return Request(
        user=_resolve_user(http_request),
        request_params=_build_request_params(http_request, url_kwargs),
        context_params={'protocol': 'http',
                        'timezone': conf.settings.TIME_ZONE,
                        },
        data=request_data,
        request_headers=http_request.META,
        request_body=request_body
    )
