import copy

from rip.request import Request
from rip.schema.base_field import BaseField, FieldTypes


class SubResourceField(BaseField):
    def __init__(self, resource_cls,
                 related_filter,
                 required=False,
                 nullable=True,
                 entity_attribute='id',
                 show_in_list=True):
        """
        In case you want to show the content of resource1 as a part of resource2
        sub-resource on resource2 is the way to go. This is not recommended at
        all. It is better to do views that collate information from multiple
        resources rather than adding sub resources.

        :param resource_cls:
        :param parent_schema_cls: the schema on which the sub-resource exists
        :param required:
        :param nullable:
        :param entity_attribute: the attribute on
        :return:
        """
        super(SubResourceField, self).__init__(required=required,
                                               nullable=nullable,
                                               entity_attribute=entity_attribute,
                                               field_type=FieldTypes.READONLY,
                                               show_in_list=show_in_list)
        self.related_filter = related_filter
        self.resource_cls = resource_cls
        self.null_return_value = None

    def get_data(self, resource_obj, request):
        return resource_obj.read_detail(request)

    def get_data_from_response(self, response):
        return response.data

    def serialize(self, request, value):
        new_context_params = {}

        #make a copy of the api_breadcrumbs and append current resource
        breadcrumbs = copy.deepcopy(
            request.context_params.get('api_breadcrumbs', []))
        breadcrumbs.append((self.schema_cls._meta.schema_name, value))
        breadcrumb_filters = copy.deepcopy(
            request.context_params.get('api_breadcrumb_filters',{}))
        breadcrumb_filters.update({self.related_filter: value,
                                   'offset': 0,
                                   'limit': 0}) #get all objects

        new_context_params.update(api_breadcrumbs = breadcrumbs,
                                  api_breadcrumb_filters=breadcrumb_filters)

        for key, value in request.context_params.items():
            if isinstance(value, (basestring, int, long)):
                new_context_params[key] = value

        request = Request(user=request.user,
                          request_params=breadcrumb_filters,
                          context_params=new_context_params)

        resource_obj = self.resource_cls()
        response = self.get_data(resource_obj, request)
        if response.is_success:
            return self.get_data_from_response(response)
        elif self.nullable:
            return self.null_return_value
        else:
            raise TypeError(
                "`{}` subResource returned unsuccessful response with {}".format(
                    self.resource_cls, response))

