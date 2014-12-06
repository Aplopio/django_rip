from rip.request import Request
from rip.response import Response

__all__ = ["PipelineComposer"]


class PipelineComposer(object):
    """
    An action helps to compose a series of handlers into a pipeline. The output of a handler is passed as the input
    to the next handler. If a handler returns a reponse, the pipeline is exited and the response returned.
    """

    def __init__(self, name=None, pipeline=None):
        self.name = name
        self.pipeline = pipeline or []

    def __call__(self, request):

        pipeline = self.pipeline

        for counter, handler in enumerate(pipeline):
            response = handler(request=request)
            assert type(response) in [Request, Response], \
                "handle_request of {handler_name} handler did not return a request or a response object".format(
                    handler_name=str(handler))
            if isinstance(response, Response):
                break

        assert isinstance(response, Response), \
            "pipeline `{pipeline_name}` did not return a response object".format(
                pipeline_name=self.name)

        return response


def compose_pipeline(name, pipeline):
    return PipelineComposer(name=name, pipeline=pipeline)
