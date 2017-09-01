import collections

from rip.crud.crud_actions import CrudActions
from rip.generic_steps import error_types, filter_operators
from rip.response import Response

SPECIAL_FILTERS = ['offset', 'limit', 'aggregate_by', 'order_by']


class DefaultRequestParamsValidation(object):
    def __init__(self, resource):
        self.resource = resource
        self.aggregate_by_fields = resource.get_meta().aggregate_by_fields
        self.order_by_fields = resource.get_meta().order_by_fields
        self.filter_by_fields = resource.get_meta().filter_by_fields

    def validate_order_by(self, request_params):
        order_by_params = request_params.get('order_by', [])
        order_by_params = filter_operators.transform_to_list(order_by_params)

        validation_errors = {}
        for order_by_field_name in order_by_params:
            field_name, order_by_type = filter_operators. \
                split_to_field_and_order_type(order_by_field_name)
            if field_name not in self.order_by_fields:
                validation_errors.update(
                    {field_name: "Ordering not allowed"})
        if validation_errors:
            return validation_errors

        return None

    def validate_aggregate_by(self, request_params):
        aggregate_by_params = request_params.get('aggregate_by', [])
        aggregate_by_params = filter_operators.transform_to_list(
            aggregate_by_params)
        validation_errors = {}

        if len(aggregate_by_params) == 0:
            validation_errors.update(
                    {'__all__': "Aggregating requires a field"})

        for field_name in aggregate_by_params:
            if field_name not in self.aggregate_by_fields:
                validation_errors.update(
                    {field_name: "Aggregating by this field is not allowed"})
        if validation_errors:
            return validation_errors
        return None

    def validate_offset(self, request_params):
        try:
            offset = request_params.get('offset', 0)
            if int(offset) < 0:
                raise ValueError
        except ValueError:
            return {'limit': 'Positive integer required'}

        return None

    def validate_limit(self, request_params):

        try:
            limit = request_params.get('limit', 20)
            if int(limit) < 0:
                raise ValueError
        except ValueError:
            return {'limit': 'Positive integer required'}

        return None

    def validate_request_params(self, request):
        request_params = request.request_params
        crud_action = request.context_params['crud_action']
        validation_errors = self._validate_fields(request_params)
        if validation_errors is None and crud_action == CrudActions.READ_LIST:
            validation_errors = self.validate_order_by(request_params)
        if validation_errors is None and \
                crud_action == CrudActions.GET_AGGREGATES:
            validation_errors = self.validate_aggregate_by(request_params)
        if validation_errors is None and crud_action == CrudActions.READ_LIST:
            validation_errors = self.validate_limit(request_params) or \
                                self.validate_offset(request_params)

        if validation_errors:
            return Response(is_success=False,
                            reason=error_types.InvalidData,
                            data=validation_errors)
        return request

    def _validate_fields(self, request_params):
        allowed_filters = self.filter_by_fields

        special_filters = SPECIAL_FILTERS
        validation_errors = {}
        for filter_name in request_params:
            if filter_name in special_filters:
                continue

            field_name, filter_type = filter_operators. \
                split_to_field_and_filter_type(filter_name)
            if field_name not in allowed_filters:
                validation_errors.update(
                    {field_name: "Filtering not allowed"})
                continue

            allowed_filter_types = allowed_filters[field_name]
            if not isinstance(allowed_filter_types, (list, tuple, set)):
                allowed_filter_types = (allowed_filter_types,)

            if field_name in allowed_filters and filter_type and \
                    filter_type not in allowed_filter_types:
                validation_errors.update(
                    {field_name: "Operator {} on field {} not allowed".
                        format(filter_type, field_name)})
                continue

        if validation_errors:
            return validation_errors

        return None
