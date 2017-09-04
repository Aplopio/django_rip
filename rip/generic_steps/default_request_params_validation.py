from rip import filter_operators
from rip.response import Response
from rip import error_types


SPECIAL_FILTERS = ['offset', 'limit', 'aggregate_by', 'order_by']

class DefaultRequestParamsValidation(object):
    def __init__(self, schema_cls, filter_by_fields, order_by_fields, aggregate_by_fields):
        self.aggregate_by_fields = aggregate_by_fields
        self.order_by_fields = order_by_fields
        self.filter_by_fields = filter_by_fields
        self.schema_cls = schema_cls

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
        validation_errors = self._validate_fields(request_params)
        if validation_errors is None:
            validation_errors = self.validate_order_by(request_params)
        if validation_errors is None:
            validation_errors = self.validate_aggregate_by(request_params)
        if validation_errors is None:
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
            field_name, filter_type = filter_operators. \
                split_to_field_and_filter_type(filter_name)
            if field_name not in allowed_filters and \
                            field_name not in special_filters:
                validation_errors.update(
                    {field_name: "Filtering not allowed"})

        if validation_errors:
            return validation_errors

        return None