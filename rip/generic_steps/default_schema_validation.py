from rip.crud.crud_actions import CrudActions
from rip.response import Response
from rip.schema.default_field_value import \
    DEFAULT_FIELD_VALUE
from rip import error_types


class DefaultSchemaValidation(object):

    def __init__(self, schema_cls):
        self.schema_cls = schema_cls

    def _get_fields_to_validate_data(self, request, data):
        action = request.context_params['crud_action']
        non_read_only_fields = self.schema_cls.non_readonly_fields()
        if action == CrudActions.UPDATE_DETAIL:
            updatable_fields = self.schema_cls.updatable_fields()
            field_names = set(data).intersection(set(updatable_fields))
        elif action == CrudActions.CREATE_DETAIL:
            field_names = non_read_only_fields.keys()
        else:
            field_names = []
        return {field_name: non_read_only_fields[field_name]
                for field_name in field_names}

    def validate_data(self, request, data):
        errors = {}
        fields_to_validate = self._get_fields_to_validate_data(request, data)
        for field_name, field in fields_to_validate.items():
            validation_result = field.validate(
                request,
                data.get(field_name, DEFAULT_FIELD_VALUE))
            if not validation_result.is_success:
                errors[field_name] = validation_result.reason

        if errors:
            return errors
        else:
            return None

    def validate_request_data(self, request):
        data_to_validate = request.data
        errors = self.validate_data(request, data=data_to_validate)
        if errors:
            return Response(is_success=False, reason=error_types.InvalidData,
                            data=errors)
        else:
            return request
