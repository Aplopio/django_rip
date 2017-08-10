from django.views import View
from django_adapter import default_rip_action_resolver
from django_adapter import default_rip_request_builder
from django_adapter.default_http_response_builder import \
    DefaultHttpResponseBuilder
from django_adapter.default_rip_action_resolver import DefaultRipActionResolver
from django_adapter.default_rip_request_builder import DefaultRipRequestBuilder
from rip.crud.crud_resource import CrudResource
from rip.generic_steps import error_types
from rip.response import Response


class DjangoCrudResource(View, CrudResource):
    # todo: override the EntityActions to allow fetching Data from Models

    # resource_name is used by the router to construct the url name when
    # adding to urls `{resource_name}-detail`, `{resource_name}-list` and
    # `{resource_name}-aggregates` will be the url names.
    # If not set, it will default to the name of the resource pluralized

    resource_name = None
    HttpResponseBuilder = DefaultHttpResponseBuilder
    RipRequestBuilder = DefaultRipRequestBuilder
    RipActionResolver = DefaultRipActionResolver

    def __init__(self, **kwargs):
        View.__init__(self, **kwargs)
        CrudResource.__init__(self)

    def dispatch(self, http_request, **url_kwargs):
        """
        :param http_request: Django http request
        :param url_kwargs:
        1. contains url_type from arguments passed to django.conf.urls.url
            when router constructs the url
        2. contains any other variables extracted from
            url like `id`, `job_id` etc.
        :return: http_response
        """
        url_type = url_kwargs.pop('url_type', None)
        action_resolver = self.RipActionResolver(
            http_request, url_type, url_kwargs)
        action_name = action_resolver.get_action_name()

        rip_request_builder = self.RipRequestBuilder(http_request, url_kwargs)
        rip_request = rip_request_builder.build_rip_request_or_response()

        if action_name is None:
            rip_response = Response(is_success=False,
                                    reason=error_types.ActionForbidden)
        elif isinstance(rip_request, Response):
            rip_response = rip_request
        else:
            rip_response = self.run_crud_action(action_name, rip_request)

        http_response_builder = self.HttpResponseBuilder(
            http_request, rip_response)
        return http_response_builder.build_http_response()
