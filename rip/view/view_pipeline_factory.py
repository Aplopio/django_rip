from rip import pipeline_composer
from rip.crud.crud_actions import CrudActions


def read_pipeline(configuration):
    view_actions = configuration['view_actions']
    authentication = configuration['authentication']
    authorization = configuration['authorization']
    serializer = configuration['serializer']
    post_action_hooks = configuration['post_action_hooks']
    response_converter = configuration['response_converter']

    pipeline = pipeline_composer.compose_pipeline(
        name=CrudActions.READ_LIST,
        pipeline=[
            authentication.authenticate,
            authorization.authorize_read,
            view_actions.read,
            serializer.serialize_detail,
            post_action_hooks.read_detail_hook,
            response_converter.convert_serialized_data_to_response
        ])

    return pipeline
