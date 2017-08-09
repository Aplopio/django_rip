from django.views import View
from django_adapter import django_response_builder
from django_adapter import rip_action_resolver
from django_adapter import rip_request_builder
from rip.crud.crud_resource import CrudResource
from rip.generic_steps import error_types
from rip.response import Response


class DjangoCrudResource(View, CrudResource):
    # todo: override the EntityActions to allow fetching Data from Models

    # resource name is the only way to know how to reverse the url of a resource
    # `{resource_name}-detail`, `{resource_name}-list` and
    # `{resource_name}-aggregates` will be the url names of generated urls for
    # a resource.
    # If not set, it will default to the name of the resource pluralized when
    # the resource class is registered with a router

    resource_name = None

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
        action_name = rip_action_resolver.get_action_name(
            http_request, url_type, url_kwargs)
        rip_request = rip_request_builder.build_rip_request_or_response(
            http_request, url_kwargs=url_kwargs)

        if action_name is None:
            rip_response = Response(is_success=False,
                                    reason=error_types.ActionForbidden)
        elif isinstance(rip_request, Response):
            rip_response = rip_request
        else:
            rip_response = self.run_crud_action(action_name, rip_request)

        return django_response_builder.build_http_response(
            http_request, rip_response)
