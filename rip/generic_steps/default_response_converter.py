from rip.response import Response


class DefaultResponseConstructor(object):
    def __init__(self, resource):
        self.resource = resource

    def convert_serialized_data_to_response(self, request):
        return Response(is_success=True,
                        data=request.context_params['serialized_data'])

    def convert_to_simple_response(self, request):
        return Response(is_success=True)
