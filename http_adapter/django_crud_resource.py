from django.views import View
from http_adapter.default_http_response_builder import \
    DefaultHttpResponseBuilder
from http_adapter.default_rip_action_resolver import DefaultRipActionResolver
from http_adapter.default_rip_request_builder import DefaultRipRequestBuilder
from model_adapter.model_data_manager import ModelDataManager
from rip.crud.crud_resource import CrudResource, CustomDataMixin
from rip.generic_steps import error_types
from rip.response import Response
from rip.schema_fields.field_types import FieldTypes
from rip.schema_fields.integer_field import IntegerField


class DjangoResource(View, CrudResource):
    # todo: override the EntityActions to allow fetching Data from Models

    # resource_name is used by the router to construct the url name when
    # adding to urls `{resource_name}-detail`, `{resource_name}-list` and
    # `{resource_name}-aggregates` will be the url names.
    # If not set, it will default to the name of the resource pluralized

    class Meta:
        http_response_builder_cls = DefaultHttpResponseBuilder
        rip_request_builder_cls = DefaultRipRequestBuilder
        rip_action_resolver_cls = DefaultRipActionResolver

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
        action_resolver = self.get_meta().rip_action_resolver_cls(
            http_request, url_type, url_kwargs)
        action_name = action_resolver.get_action_name()

        rip_request_builder = self.get_meta().rip_request_builder_cls(
            http_request, url_kwargs)
        rip_request = rip_request_builder.build_rip_request_or_response()

        if action_name is None:
            rip_response = Response(is_success=False,
                                    reason=error_types.ActionForbidden)
        elif isinstance(rip_request, Response):
            rip_response = rip_request
        else:
            rip_response = self.run_crud_action(action_name, rip_request)

        http_response_builder = self.get_meta().http_response_builder_cls(
            http_request, rip_response)
        return http_response_builder.build_http_response()


class DjangoModelResource(DjangoResource):
    id = IntegerField(field_type=FieldTypes.IMMUTABLE, nullable=False)

    class Meta:
        data_manager_cls = ModelDataManager
        model_cls = None

    def get_data_manager(self):
        return self._meta.data_manager_cls(
            resource=self)


class CustomDataResource(DjangoResource, CustomDataMixin):
    pass
