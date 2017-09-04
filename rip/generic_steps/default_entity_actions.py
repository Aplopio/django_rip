from django.conf import settings
from rip.response import Response
from rip import error_types


class DefaultEntityActions(object):
    """
    Defines the default steps needed for actions  on a CRUD entity
    """
    request_filters_property = 'request_filters'
    list_property_name = 'entities'
    get_aggregates_property_name = 'entity_aggregates'
    entity_list_total_count_property_name = 'total_count'
    detail_property_name = 'entity'
    updated_property_name = 'entity'

    def __init__(self, schema_cls, default_offset, default_limit):
        self.schema_cls = schema_cls
        self.default_limit = default_limit
        self.default_offset = default_offset

    def get_limit_and_offset(self, request_filters):
        default_limit =  self.default_limit
        default_offset = self.default_offset
        limit = int(request_filters.get('limit', default_limit))
        if limit == 0:
            # for legacy reasons, if limit 0 is specified, we want to treat
            # it like no limit
            limit = None
        offset = int(request_filters.get('offset', default_offset))
        return dict(limit=limit, offset=offset)

    def read_list(self, request):
        """
        :param request: an apiv2 request object
        :return: request if successful with entities set on request
        """
        request_filters = request.context_params.get(
            self.request_filters_property, {})
        request_filters.update(**self.get_limit_and_offset(request_filters))
        entities = self.get_entity_list(request, **request_filters)
        request.context_params[self.list_property_name] = entities

        # offset and limit don't make sense to get aggregates
        count_request_filters = request_filters.copy()
        count_request_filters.pop('offset', None)
        count_request_filters.pop('limit', None)
        count_request_filters.pop('order_by', None)
        total_count = self.get_entity_list_total_count(request,
                                                       **count_request_filters)

        request.context_params[self.entity_list_total_count_property_name] = \
            total_count
        return request

    def read_detail(self, request):
        """

        :param request: an apiv2 request object
        :return: request if successful with entities set on request
        """
        request_filters = request.context_params.get(
            self.request_filters_property, {})
        entity = self.get_entity(request, **request_filters)
        if entity is None:
            return Response(is_success=False, reason=error_types.ObjectNotFound)

        request.context_params[self.detail_property_name] = entity

        return request

    def update_detail(self, request):
        """
        :param request: an apiv2 request object
        :return: request if successful with entities set on request
        """
        entity = request.context_params[self.detail_property_name]
        updated_entity = self.update_entity(
            request,
            entity, **request.context_params['data'])
        request.context_params[self.updated_property_name] = updated_entity
        return request

    def delete_detail(self, request):
        """

        :param request: an apiv2 request object
        :return: request if successful with entities set on request
        """
        entity = request.context_params[self.detail_property_name]
        self.delete_entity(request, entity)
        return request

    def create_detail(self, request):
        """
        :param request: an apiv2 request object
        :return: request if successful with entities set on request
        """
        entity = self.create_entity(request, **request.context_params['data'])
        request.context_params[self.detail_property_name] = entity
        return request

    def get_aggregates(self, request):
        request_filters = request.context_params[self.request_filters_property]
        request_filters['aggregate_by'] = request_filters.get('aggregate_by', [])
        aggregates = self.get_entity_aggregates(request,
                                        **request_filters)
        request.context_params[self.get_aggregates_property_name] = aggregates
        return request

    def update_entity(self, request, entity, **update_params):
        raise NotImplementedError

    def get_entity_list(self, request, **kwargs):
        raise NotImplementedError

    def get_entity_list_total_count(self, request, **kwargs):
        raise NotImplementedError

    def get_entity(self, request, **kwargs):
        entities = self.get_entity_list(request, **kwargs)
        if len(entities) == 0:
            return None
        elif len(entities) > 1:
            raise error_types.MultipleObjectsFound()
        else:
            return entities[0]

    def create_entity(self, request, **kwargs):
        raise NotImplementedError

    def delete_entity(self, request, entity):
        raise NotImplementedError

    def get_entity_aggregates(self, request, **kwargs):
        raise NotImplementedError


