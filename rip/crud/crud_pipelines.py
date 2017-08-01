from rip.crud import pipeline_composer
from rip.crud.crud_actions import CrudActions
from rip.generic_steps.default_authentication import DefaultAuthentication
from rip.generic_steps.default_authorization import DefaultAuthorization
from rip.generic_steps.default_data_cleaner import DefaultRequestCleaner
from rip.generic_steps.default_entity_actions import DefaultEntityActions
from rip.generic_steps.default_post_action_hooks import DefaultPostActionHooks
from rip.generic_steps.default_request_params_validation import \
    DefaultRequestParamsValidation
from rip.generic_steps.default_response_converter import \
    DefaultResponseConverter
from rip.generic_steps.default_schema_serializer import DefaultEntitySerializer
from rip.generic_steps.default_schema_validation import DefaultSchemaValidation


class ConfigManager(object):
    def __init__(
            self, schema_cls, authentication_cls=DefaultAuthentication,
            authorization_cls=DefaultAuthorization,
            request_params_validation_cls=DefaultRequestParamsValidation,
            schema_validation_cls=DefaultSchemaValidation,
            data_cleaner_cls=DefaultRequestCleaner,
            entity_actions_cls=DefaultEntityActions,
            post_action_hooks_cls=DefaultPostActionHooks,
            response_converter_cls=DefaultResponseConverter,
            serializer_cls=DefaultEntitySerializer,
            filter_by_fields=None,
            order_by_fields=None,
            aggregate_by_fields=None):

        self.schema_cls = schema_cls
        self.authentication = authentication_cls(schema_cls=self.schema_cls)
        self.authorization = authorization_cls(schema_cls=self.schema_cls)
        self.request_params_validation = request_params_validation_cls(
            schema_cls=schema_cls,
            filter_by_fields=filter_by_fields or {},
            order_by_fields=order_by_fields or [],
            aggregate_by_fields=aggregate_by_fields or []
        )
        self.schema_validation = schema_validation_cls(schema_cls=schema_cls)
        self.data_cleaner = data_cleaner_cls(schema_cls=schema_cls)
        self.entity_actions = entity_actions_cls(schema_cls=schema_cls)
        self.post_action_hooks = post_action_hooks_cls(schema_cls=schema_cls)
        self.response_converter = response_converter_cls(schema_cls=schema_cls)
        self.serializer = serializer_cls(schema_cls=schema_cls)


def read_detail_pipeline(config):
    get_detail_pipeline = pipeline_composer.compose_pipeline(
        name=CrudActions.READ_DETAIL,
        pipeline=[
            config.authentication.authenticate,
            config.data_cleaner.clean_data_for_read_detail,
            config.entity_actions.read_detail,
            config.authorization.authorize_read_detail,
            config.serializer.serialize_detail,
            config.post_action_hooks.read_detail_hook,
            config.response_converter.convert_serialized_data_to_response
        ])
    return get_detail_pipeline


def update_detail_pipeline(config):
    pipeline = pipeline_composer.compose_pipeline(
        name=CrudActions.UPDATE_DETAIL,
        pipeline=[
            config.authentication.authenticate,
            config.data_cleaner.clean_data_for_read_detail,
            config.data_cleaner.clean_data_for_update_detail,
            config.schema_validation.validate_request_data,
            config.entity_actions.read_detail,
            config.authorization.authorize_update_detail,
            config.serializer.serialize_detail_pre_update,
            config.entity_actions.update_detail,
            config.serializer.serialize_detail,
            config.post_action_hooks.update_detail_hook,
            config.response_converter.convert_serialized_data_to_response
        ])
    return pipeline


def create_or_update_detail_pipeline(config):
    pipeline = pipeline_composer.compose_pipeline(
        name=CrudActions.CREATE_OR_UPDATE_DETAIL,
        pipeline=[
            config.authentication.authenticate,
            config.data_cleaner.clean_data_for_read_detail,
            config.data_cleaner.clean_data_for_update_detail,
            config.schema_validation.validate_request_data,
            config.entity_actions.read_detail,
            config.authorization.authorize_update_detail,
            config.serializer.serialize_detail_pre_update,
            config.entity_actions.update_detail,
            config.serializer.serialize_detail,
            config.post_action_hooks.update_detail_hook,
            config.response_converter.convert_serialized_data_to_response
        ])
    return pipeline


def read_list_pipeline(config):
    pipeline = pipeline_composer.compose_pipeline(
        name=CrudActions.READ_LIST,
        pipeline=[
            config.authentication.authenticate,
            config.request_params_validation.validate_request_params,
            config.data_cleaner.clean_data_for_read_list,
            config.authorization.add_read_list_filters,
            config.entity_actions.read_list,
            config.serializer.serialize_list,
            config.post_action_hooks.read_list_hook,
            config.response_converter.convert_serialized_data_to_response
        ])
    return pipeline


def create_detail_pipeline(config):
    pipeline = pipeline_composer.compose_pipeline(
        name=CrudActions.CREATE_DETAIL,
        pipeline=[
            config.authentication.authenticate,
            config.data_cleaner.clean_data_for_create_detail,
            config.schema_validation.validate_request_data,
            config.authorization.authorize_create_detail,
            config.entity_actions.create_detail,
            config.serializer.serialize_detail,
            config.post_action_hooks.create_detail_hook,
            config.response_converter.convert_serialized_data_to_response
        ])

    return pipeline


def delete_detail_pipeline(config):
    pipeline = pipeline_composer.compose_pipeline(
        name=CrudActions.DELETE_DETAIL,
        pipeline=[
            config.authentication.authenticate,
            config.data_cleaner.clean_data_for_delete_detail,
            config.entity_actions.read_detail,
            config.authorization.authorize_delete_detail,
            config.entity_actions.delete_detail,
            config.post_action_hooks.delete_detail_hook,
            config.response_converter.convert_to_simple_response
        ])

    return pipeline


def get_aggregates_pipeline(config):
    pipeline = pipeline_composer.compose_pipeline(
        name=CrudActions.GET_AGGREGATES,
        pipeline=[
            config.authentication.authenticate,
            config.request_params_validation.validate_request_params,
            config.data_cleaner.clean_data_for_get_aggregates,
            config.authorization.add_read_list_filters,
            config.entity_actions.get_aggregates,
            config.serializer.serialize_entity_aggregates,
            config.post_action_hooks.get_aggregates_hook,
            config.response_converter.convert_serialized_data_to_response
        ])

    return pipeline
