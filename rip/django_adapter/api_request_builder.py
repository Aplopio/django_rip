"""
creates an api request given a django http request object
"""
from django import conf
import simplejson

from rip.django_adapter import \
    metadata_factory
from rip.request import Request
from simplejson import JSONDecodeError


def _build_request_params(http_request, breadcrumb_filters):
    request_params = {}
    for key in http_request.GET:
        value = http_request.GET.getlist(key)
        if len(value) == 1:
            value = value[0]
        request_params[key] = value

    request_params.update(breadcrumb_filters)
    return request_params


def _resolve_user(http_request):
    return http_request.user \
        if not http_request.user.is_anonymous() \
        else None


def build_request_data(request_body, request_meta):
    content_types = request_meta.get('CONTENT_TYPE', '').split(";")
    if 'application/json' in content_types:
        try:
            request_data = simplejson.loads(request_body)
        except JSONDecodeError, e:
            return {'error_message': e.message}
    else:
        request_data = {}
    return request_data


def build_request(http_request, url, api, request_data, request_body):
    endpoint = api.resolve_endpoint(url)
    breadcrumb_filters = metadata_factory.api_breadcrumb_filters(url, endpoint)
    parent_breadcrumbs = metadata_factory.api_breadcrumbs(url, endpoint)
    return Request(
        user=_resolve_user(http_request),
        request_params=_build_request_params(http_request, breadcrumb_filters),
        context_params={'protocol': 'http',
                        'url': url,
                        'api_name': api.name,
                        'api_version': api.version,
                        'timezone': conf.settings.TIME_ZONE,
                        'api_breadcrumbs': parent_breadcrumbs},
        data=request_data,
        request_headers=http_request.META,
        request_body=request_body)
