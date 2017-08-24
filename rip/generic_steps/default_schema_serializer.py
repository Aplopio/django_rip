"""
serializes an entity or a list of entities to response data
"""

from rip.crud.crud_actions import CrudActions
from rip.generic_steps import filter_operators
from rip.generic_steps.attribute_getter import DefaultEntityAttributeManager


class DefaultEntitySerializer(object):
    entity_list_var = 'entities'
    entity_var = 'entity'
    aggregates_var = 'entity_aggregates'
    serialized_data_var = 'serialized_data'
    serialized_data_var_pre_update = 'serialized_data_pre_update'

    def __init__(self, resource,
                 attribute_getter_cls=DefaultEntityAttributeManager):
        self.resource = resource
        self.default_offset = resource.get_meta().default_offset
        self.default_limit = resource.get_meta().default_limit
        self.attribute_getter_cls = attribute_getter_cls

    def get_fields_to_serialize(self, request):
        schema_fields = self.resource.all_fields()
        if request.context_params.get('crud_action') == CrudActions.READ_LIST:
            return self.resource.list_fields()

        elif request.context_params.get('crud_action') == \
                CrudActions.GET_AGGREGATES:
            aggregate_by_fields = filter_operators.transform_to_list(
                request.request_params.get('aggregate_by', []))
            return {key: schema_fields[key] for key in aggregate_by_fields}
        return schema_fields

    def serialize_aggregated_entity(self, request, aggregate_entity):
        aggregate_by_fields = self.get_fields_to_serialize(request)
        attribute_getter = self.attribute_getter_cls(entity=aggregate_entity)
        serialized = {}
        for field_name, field in aggregate_by_fields.items():
            field_attribute = field.entity_attribute or field_name
            serialized[field_name] = \
                attribute_getter.get_attribute(field_attribute)
        serialized['count'] = aggregate_entity['count']
        return serialized

    def serialize_entity(self, request, entity):
        """
        @param: entity -> entity object returned by the entity_actions step
        """
        attribute_getter = self.attribute_getter_cls(entity=entity)
        serialized = {}
        fields_to_serialize = self.get_fields_to_serialize(request)
        for field_name, field in fields_to_serialize.items():
            field_override = getattr(self, 'serialize_%s' % field_name, None)
            if field_override:
                serialized_value = field_override(request, entity)
            else:
                entity_attribute = field.entity_attribute or field_name

                try:
                    serialized_value = attribute_getter.get_attribute(
                        entity_attribute)
                except AttributeError as ex:
                    if field.required:
                        raise ex
                    continue

            serialized[field_name] = field.serialize(request, serialized_value)
        return serialized

    def serialize_detail(self, request):
        """
        @param: request -> request object that will be converted into a response
        @param: schema_obj_variable -> property name of the schema_fields object on
        request obj that needs to be serialized
        """
        schema_obj = request.context_params[self.entity_var]
        data = self.serialize_entity(request, schema_obj)
        request.context_params[self.serialized_data_var] = data
        return request

    def serialize_detail_pre_update(self, request):
        entity = request.context_params[self.entity_var]
        data = self.serialize_entity(request, entity)
        request.context_params[self.serialized_data_var_pre_update] = data
        return request

    def serialize_list(self, request):
        """
        @param: request -> request object that will be converted into a response
        """
        entity_list = request.context_params[self.entity_list_var]
        serialized_objects = [self.serialize_entity(request, entity) for
                              entity in entity_list]
        request_filters = request.context_params.get('request_filters', {})
        serialized_meta = {'offset': int(
            request_filters.get('offset', self.default_offset)),
                           # handles null case. Legacy requirements
                           'limit': int(
            request_filters.get('limit', self.default_limit)),
                           'total': request.context_params['total_count']}

        data = dict(meta=serialized_meta,
                    objects=serialized_objects)

        request.context_params[self.serialized_data_var] = data
        return request

    def serialize_entity_aggregates(self, request):
        aggregates = request.context_params[self.aggregates_var]
        serialized_data = [self.serialize_aggregated_entity(request, aggregate)
                           for aggregate in aggregates]

        request.context_params[self.serialized_data_var] = serialized_data
        return request
