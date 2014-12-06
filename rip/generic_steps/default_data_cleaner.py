from rip import filter_operators
from rip.crud.crud_actions import CrudActions


class DefaultRequestCleaner(object):

    def __init__(self, schema_cls):
        self.schema_cls = schema_cls

    def _get_attribute_name(self, field_name):
        fields = self.schema_cls._meta.fields
        if field_name not in fields:
            cleaned_field_name = field_name
        else:
            field_obj = fields[field_name]
            cleaned_field_name = field_obj.entity_attribute or field_name
        return cleaned_field_name


    def _get_filter_value(self, request, field_name, value, filter_type):
        from rip.schema.schema_field import SchemaField
        from rip.schema.list_field import ListField

        schema_cls = self.schema_cls
        field_name_split = field_name.split(filter_operators.OPERATOR_SEPARATOR)
        cleaned_field_value = value
        for part in field_name_split:
            fields = schema_cls._meta.fields
            field_obj = fields.get(part)
            if isinstance(field_obj, SchemaField):
                schema_cls = field_obj.of_type
                continue

            if field_obj is not None:
                if isinstance(value, list) and not isinstance(field_obj,
                                                              ListField):
                    cleaned_field_value = [field_obj.clean(request, val_item)
                                           for val_item in value]
                elif isinstance(field_obj, ListField):
                    cleaned_field_value = field_obj.clean(request, value) if isinstance(value, list) else [value]
                else:
                    cleaned_field_value = field_obj.clean(request, value)
                break

        return cleaned_field_value

    def clean_request_params(self, request):
        request_params = request.request_params
        request_filters = {}
        for filter_name in request_params.keys():
            field_name, filter_type = filter_operators. \
                split_to_field_and_filter_type(filter_name)

            cleaned_field_value = self._get_filter_value(
                request, field_name, request_params[filter_name], filter_type)

            attribute_name = self._get_attribute_name(field_name)
            if filter_type is not None:
                attribute_name = filter_operators.OPERATOR_SEPARATOR.join(
                    [attribute_name, filter_type])

            request_filters[attribute_name] = cleaned_field_value

        if 'order_by' in request_filters:
            order_by = filter_operators.transform_to_list(request_filters[
                'order_by'])
            request_filters['order_by'] = \
                [self._get_attribute_name(field_name)
                 for field_name in order_by]
        if 'aggregate_by' in request_filters:
            aggregate_by = filter_operators.transform_to_list(request_filters[
                'aggregate_by'])
            request_filters['aggregate_by'] = \
                [self._get_attribute_name(field_name)
                 for field_name in aggregate_by]
            
        return request_filters

    def clean_data_for_read_detail(self, request):
        return self.clean_data_for_read_list(request)

    def clean_data_for_delete_detail(self, request):
        return self.clean_data_for_read_list(request)

    def clean_data_for_read_list(self, request):
        request_filters = self.clean_request_params(request)
        request.context_params['request_filters'] = request_filters
        return request

    def clean_data_for_get_aggregates(self, request):
        return self.clean_data_for_read_detail(request)

    def _get_fields_to_clean(self, request, data):
        action = request.context_params['crud_action']
        non_read_only_fields = self.schema_cls.non_readonly_fields()

        if action == CrudActions.UPDATE_DETAIL:
            updatable_fields = self.schema_cls.updatable_fields()
            field_names = set(data).intersection(set(updatable_fields))
        elif action == CrudActions.CREATE_DETAIL:
            field_names = set(data).intersection(set(non_read_only_fields))
        else:
            field_names = []

        return {field_name: non_read_only_fields[field_name]
                for field_name in field_names}

    def clean_data_for_update_detail(self, request):
        data = request.data
        request.context_params['data'] = self.clean(request,
                                                    data)
        return request

    def clean_data_for_create_detail(self, request):
        data = request.data
        request.context_params['data'] = self.clean(request,
                                                    data)
        request = self.clean_data_for_read_detail(request)
        return request

    def clean(self, request, data):
        clean_data = {}

        fields_to_clean = self._get_fields_to_clean(request, data)
        for field_name, field_obj in fields_to_clean.items():
            if field_name in data:
                clean_data[self._get_attribute_name(field_name)] = \
                    field_obj.clean(request, data[field_name])
        return clean_data