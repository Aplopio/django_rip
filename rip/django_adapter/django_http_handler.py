from functools import partial
import json

from django.http import HttpResponseNotAllowed, HttpResponseNotFound, HttpResponseBadRequest

from rip.django_adapter import django_response_builder, \
    action_resolver
from rip.django_adapter import api_request_builder


def handle_api_call(http_request, url, api):
    if not action_resolver.is_valid_resource(url, api):
        return HttpResponseNotFound()

    action = action_resolver.resolve_action(http_request, url, api)
    if action is None:
        # we could not resolve what action to call for this http request.
        # return method not allowed response
        return HttpResponseNotAllowed("%s:%s" % (url, http_request.method))

    request_body = http_request.read()
    request_data = api_request_builder.build_request_data(request_body, http_request.META)
    if request_data.get('error_message'):
        return HttpResponseBadRequest(
            json.dumps(request_data), content_type='application/json')

    request = api_request_builder.build_request(http_request=http_request,
                                                url=url, api=api,
                                                request_data=request_data,
                                                request_body=request_body)

    response = action(request)

    http_response = django_response_builder.build_http_response(
        http_request, response)
    return http_response


def create_http_handler(api):
    return partial(handle_api_call, api=api)
