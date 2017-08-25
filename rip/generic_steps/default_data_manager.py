from rip.generic_steps import error_types
from rip.response import Response, NotFoundResponse, ActionForbiddenResponse


class DefaultDataManager(object):
    """
    Defines the default steps needed for actions  on a CRUD entity
    """
    request_filters_property = 'request_filters'
    list_property_name = 'entities'
    get_aggregates_property_name = 'entity_aggregates'
    entity_list_total_count_property_name = 'total_count'
    detail_property_name = 'entity'
    updated_property_name = 'entity'

    def __init__(self, resource):
        self.resource = resource
        self.default_limit = resource.get_meta().default_limit
        self.default_offset = resource.get_meta().default_offset

    def get_limit_and_offset(self, request_filters):
        default_limit = self.default_limit
        default_offset = self.default_offset
        limit = int(request_filters.get('limit', default_limit))
        offset = int(request_filters.get('offset', default_offset))
        return dict(limit=limit, offset=offset)

    def read_list(self, request, get_entity_list_fn=None,
                  get_total_count_fn=None):
        """
        :param get_total_count_fn:
        :param get_entity_list_fn: If present, calls this function to get
        a list of entities instead of self.get_entity_list
        :param request: an apiv2 request object
        :return: request if successful with entities set on request
        """
        request_filters = request.context_params.get(
            self.request_filters_property, {})
        list_filters = request_filters.copy()
        list_filters.pop('order_by', None)
        list_filters.update(**self.get_limit_and_offset(request_filters))
        entity_list_getter = get_entity_list_fn or self.get_entity_list
        entities_response = entity_list_getter(request, **list_filters)

        if entities_response is error_types.ActionForbidden:
            return ActionForbiddenResponse()

        request.context_params[self.list_property_name] = entities_response

        # offset and limit don't make sense to get aggregates
        count_filters = request_filters.copy()
        count_filters.pop('offset', None)
        count_filters.pop('limit', None)
        count_filters.pop('order_by', None)
        total_count_getter = get_total_count_fn or \
                             self.get_entity_list_total_count
        total_count_response = total_count_getter(request, **count_filters)

        if total_count_response is error_types.ActionForbidden:
            return ActionForbiddenResponse()

        request.context_params[self.entity_list_total_count_property_name] = \
            total_count_response
        return request

    def read_detail(self, request, get_entity_fn=None):
        """
        :param get_entity_fn: If present, calls this function to get
        an entity instead of self.get_entity
        :param request: an apiv2 request object
        :return: request if successful with entities set on request
        """
        request_filters = request.context_params.get(
            self.request_filters_property, {})

        entity_getter = get_entity_fn or self.get_entity
        entity_response = entity_getter(request, **request_filters)

        if entity_response in (error_types.ObjectNotFound, None):
            return NotFoundResponse()
        elif entity_response is error_types.ActionForbidden:
            return ActionForbiddenResponse()

        request.context_params[self.detail_property_name] = entity_response
        return request

    def update_detail(self, request, update_entity_fn=None):
        """
        :param update_entity_fn: If present, calls this override
        to update the entity instead of self.update_entity
        :param request: an apiv2 request object
        :return: request if successful with entities set on request
        """
        entity = request.context_params[self.detail_property_name]

        entity_updater = update_entity_fn or self.update_entity
        entity_response = entity_updater(
                request, entity, **request.context_params['data'])

        if entity_response is error_types.ActionForbidden:
            return ActionForbiddenResponse()

        request.context_params[self.updated_property_name] = entity_response
        return request

    def delete_detail(self, request, delete_entity_fn=None):
        """
        :param delete_entity_fn: If present, calls this function to delete
        an entity instead of self.delete_entity
        :param request: an apiv2 request object
        :return: request if successful with entities set on request
        """
        entity = request.context_params[self.detail_property_name]
        entity_deleter = delete_entity_fn or self.delete_entity
        entity_response = entity_deleter(request, entity)
        if entity_response is error_types.ActionForbidden:
            return ActionForbiddenResponse()

        return request

    def create_detail(self, request, create_entity_fn=None):
        """
        :param create_entity_fn: If present, calls this function to create
        an entity instead of self.create_entity
        :param request: an apiv2 request object
        :return: request if successful with entities set on request
        """
        entity_creator = create_entity_fn or self.create_entity
        entity_response = entity_creator(
            request, **request.context_params['data'])

        if entity_response is error_types.ActionForbidden:
            return ActionForbiddenResponse()

        request.context_params[self.detail_property_name] = entity_response
        return request

    def get_aggregates(self, request, get_aggregates_fn=None):
        request_filters = request.context_params[self.request_filters_property]
        request_filters['aggregate_by'] = request_filters.get('aggregate_by', [])
        aggregates_getter = get_aggregates_fn or self.get_entity_aggregates
        aggregates_response = aggregates_getter(request, **request_filters)

        if aggregates_response is error_types.ActionForbidden:
            return ActionForbiddenResponse()

        request.context_params[self.get_aggregates_property_name] = \
            aggregates_response
        return request

    def update_entity(self, request, entity, **update_params):
        raise NotImplementedError

    def get_entity_list(self, request, limit, offset, **kwargs):
        raise NotImplementedError

    def get_entity_list_total_count(self, request, **kwargs):
        raise NotImplementedError

    def get_entity(self, request, **kwargs):
        kwargs['limit'] = 2
        kwargs['offset'] = 0
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


