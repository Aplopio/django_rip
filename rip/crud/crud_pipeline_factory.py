from rip.crud.crud_actions import CrudActions
from rip import pipeline_composer


def read_detail_pipeline(configuration):
    entity_actions = configuration['entity_actions']
    authentication = configuration['authentication']
    authorization = configuration['authorization']
    serializer = configuration['serializer']
    data_cleaner = configuration['data_cleaner']
    post_action_hooks = configuration['post_action_hooks']
    response_converter = configuration['response_converter']

    get_detail_pipeline = pipeline_composer.compose_pipeline(
        name=CrudActions.READ_DETAIL,
        pipeline=[
            authentication.authenticate,
            data_cleaner.clean_data_for_read_detail,
            entity_actions.read_detail,
            authorization.authorize_read_detail,
            serializer.serialize_detail,
            post_action_hooks.read_detail_hook,
            response_converter.convert_serialized_data_to_response
        ])

    return get_detail_pipeline


def update_detail_pipeline(configuration):
    entity_actions = configuration['entity_actions']
    authentication = configuration['authentication']
    authorization = configuration['authorization']
    schema_validation = configuration['schema_validation']
    serializer = configuration['serializer']
    data_cleaner = configuration['data_cleaner']
    post_action_hooks = configuration['post_action_hooks']
    response_converter = configuration['response_converter']

    update_detail_pipeline = pipeline_composer.compose_pipeline(
        name=CrudActions.UPDATE_DETAIL,
        pipeline=[
            authentication.authenticate,
            data_cleaner.clean_data_for_read_detail,
            data_cleaner.clean_data_for_update_detail,
            schema_validation.validate_request_data,
            entity_actions.read_detail,
            authorization.authorize_update_detail,
            serializer.serialize_detail_pre_update,
            entity_actions.update_detail,
            serializer.serialize_detail,
            post_action_hooks.update_detail_hook,
            response_converter.convert_serialized_data_to_response
        ])

    return update_detail_pipeline


def read_list_pipeline(configuration):
    entity_actions = configuration['entity_actions']
    request_params_validation = configuration['request_params_validation']
    authentication = configuration['authentication']
    authorization = configuration['authorization']
    serializer = configuration['serializer']
    data_cleaner = configuration['data_cleaner']
    post_action_hooks = configuration['post_action_hooks']
    response_converter = configuration['response_converter']

    read_list_pipeline = pipeline_composer.compose_pipeline(
        name=CrudActions.READ_LIST,
        pipeline=[
            authentication.authenticate,
            request_params_validation.validate_request_params,
            data_cleaner.clean_data_for_read_list,
            authorization.add_read_list_filters,
            entity_actions.read_list,
            serializer.serialize_list,
            post_action_hooks.read_list_hook,
            response_converter.convert_serialized_data_to_response
        ])

    return read_list_pipeline


def create_detail_pipeline(configuration):
    entity_actions = configuration['entity_actions']
    authentication = configuration['authentication']
    authorization = configuration['authorization']
    schema_validation = configuration['schema_validation']
    serializer = configuration['serializer']
    data_cleaner = configuration['data_cleaner']
    post_action_hooks = configuration['post_action_hooks']
    response_converter = configuration['response_converter']

    create_detail_pipeline = pipeline_composer.compose_pipeline(
        name=CrudActions.CREATE_DETAIL,
        pipeline=[
            authentication.authenticate,
            data_cleaner.clean_data_for_create_detail,
            schema_validation.validate_request_data,
            authorization.authorize_create_detail,
            entity_actions.create_detail,
            serializer.serialize_detail,
            post_action_hooks.create_detail_hook,
            response_converter.convert_serialized_data_to_response
        ])

    return create_detail_pipeline


def delete_detail_pipeline(configuration):
    entity_actions = configuration['entity_actions']
    authentication = configuration['authentication']
    authorization = configuration['authorization']
    data_cleaner = configuration['data_cleaner']
    post_action_hooks = configuration['post_action_hooks']
    response_converter = configuration['response_converter']

    delete_detail_pipeline = pipeline_composer.compose_pipeline(
        name=CrudActions.DELETE_DETAIL,
        pipeline=[
            authentication.authenticate,
            data_cleaner.clean_data_for_delete_detail,
            entity_actions.read_detail,
            authorization.authorize_delete_detail,
            entity_actions.delete_detail,
            post_action_hooks.delete_detail_hook,
            response_converter.convert_to_simple_response
        ])

    return delete_detail_pipeline


def get_aggregates_pipeline(configuration):
    entity_actions = configuration['entity_actions']
    authentication = configuration['authentication']
    request_params_validation = configuration['request_params_validation']
    authorization = configuration['authorization']
    serializer = configuration['serializer']
    data_cleaner = configuration['data_cleaner']
    post_action_hooks = configuration['post_action_hooks']
    response_converter = configuration['response_converter']

    get_aggregates_pipeline = pipeline_composer.compose_pipeline(
        name=CrudActions.GET_AGGREGATES,
        pipeline=[
            authentication.authenticate,
            request_params_validation.validate_request_params,
            data_cleaner.clean_data_for_get_aggregates,
            authorization.add_read_list_filters,
            entity_actions.get_aggregates,
            serializer.serialize_entity_aggregates,
            post_action_hooks.get_aggregates_hook,
            response_converter.convert_serialized_data_to_response
        ])

    return get_aggregates_pipeline
