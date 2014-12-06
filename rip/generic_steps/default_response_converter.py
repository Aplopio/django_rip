from rip.response import Response


class DefaultResponseConverter(object):

    def __init__(self, schema_cls):
        self.schema_cls = schema_cls

    def convert_serialized_data_to_response(self, request):
        return Response(is_success=True,
                        data=request.context_params['serialized_data'])

    def convert_to_simple_response(self, request):
        return Response(is_success=True)