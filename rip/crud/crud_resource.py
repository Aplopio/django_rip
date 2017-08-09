from rip.crud.crud_actions import CrudActions
from rip.crud.pipeline_composer import PipelineComposer
from rip.generic_steps import error_types
from rip.generic_steps.default_authentication import DefaultAuthentication
from rip.generic_steps.default_authorization import DefaultAuthorization
from rip.generic_steps.default_data_cleaner import DefaultRequestCleaner
from rip.generic_steps.default_entity_actions import DefaultEntityActions
from rip.generic_steps.default_post_action_hooks import DefaultPostActionHooks
from rip.generic_steps.default_request_params_validation import \
    DefaultRequestParamsValidation
from rip.generic_steps.default_response_converter import \
    DefaultResponseConstructor
from rip.generic_steps.default_schema_serializer import DefaultEntitySerializer
from rip.generic_steps.default_schema_validation import DefaultSchemaValidation
from rip.response import Response


class CrudResource(object):
    """
    Defines a Resource with CRUD actions implemented in as as series of steps
    in a pipeline
    If your resource confirms to the basic CRUD actions in Rest,
    then inherit from this class
    """

    schema_cls = None
    # By default only allow Read actions. Subclasses are expected
    # to override this to allow update/delete etc.
    allowed_actions = [CrudActions.READ_DETAIL, CrudActions.READ_LIST]
    filter_by_fields = {}
    order_by_fields = []
    aggregate_by_fields = []
    default_offset = 0
    default_limit = 20

    RequestAuthentication = DefaultAuthentication
    RequestAuthorization = DefaultAuthorization
    RequestParamsValidation = DefaultRequestParamsValidation
    SchemaValidation = DefaultSchemaValidation
    RequestCleaner = DefaultRequestCleaner
    EntityActions = DefaultEntityActions
    EntitySerializer = DefaultEntitySerializer
    PostActionHooks = DefaultPostActionHooks
    ResponseConstructor = DefaultResponseConstructor

    def __new__(cls, *args, **kwargs):
        if cls.schema_cls is None:
            raise TypeError('Missing configuration property `schema_cls` \
                             on Resource `{resource_name}`'
                            .format(resource_name=cls.__name__))
        obj = super(CrudResource, cls).__new__(cls, *args, **kwargs)
        return obj

    def __init__(self):
        super(CrudResource, self).__init__()

        self.request_authentication = self.RequestAuthentication(
            schema_cls=self.schema_cls)
        self.request_authorization = self.RequestAuthorization(
            schema_cls=self.schema_cls)
        self.request_params_validation = self.RequestParamsValidation(
            schema_cls=self.schema_cls, filter_by_fields=self.filter_by_fields,
            order_by_fields=self.order_by_fields,
            aggregate_by_fields=self.aggregate_by_fields)
        self.schema_validation = self.SchemaValidation(
            schema_cls=self.schema_cls)
        self.request_cleaner = self.RequestCleaner(schema_cls=self.schema_cls)
        self.entity_actions = self.EntityActions(
            schema_cls=self.schema_cls, default_offset=self.default_offset,
            default_limit=self.default_limit)
        self.entity_serializer = self.EntitySerializer(
            schema_cls=self.schema_cls)
        self.post_action_hooks = self.PostActionHooks(
            schema_cls=self.schema_cls)
        self.response_constructor = self.ResponseConstructor(
            schema_cls=self.schema_cls)

        self.pipelines = {
            CrudActions.READ_DETAIL: self.get_read_detail_pipeline(),
            CrudActions.UPDATE_DETAIL: self.get_update_detail_pipeline(),
            CrudActions.READ_LIST: self.get_read_list_pipeline(),
            CrudActions.CREATE_DETAIL: self.get_create_detail_pipeline(),
            CrudActions.CREATE_OR_UPDATE_DETAIL: self.get_create_or_update_detail_pipeline(),
            CrudActions.GET_AGGREGATES: self.get_aggregates_pipeline()
        }

    def run_crud_action(self, action_name, request):
        if action_name not in self.allowed_actions:
            return Response(
                is_success=False, reason=error_types.MethodNotAllowed)
        crud_pipeline = self.pipelines[action_name]
        return crud_pipeline(request)

    def get_read_detail_pipeline(self):
        read_detail_pipeline = [
            self.request_authentication.authenticate,
            self.request_cleaner.clean_data_for_read_detail,
            self.entity_actions.read_detail,
            self.request_authorization.authorize_read_detail,
            self.entity_serializer.serialize_detail,
            self.post_action_hooks.read_detail_hook,
            self.response_constructor.convert_serialized_data_to_response
        ]
        return PipelineComposer(
            name=CrudActions.READ_DETAIL, pipeline=read_detail_pipeline)

    def get_update_detail_pipeline(self):
        update_pipeline = [
            self.request_authentication.authenticate,
            self.request_cleaner.clean_data_for_read_detail,
            self.request_cleaner.clean_data_for_update_detail,
            self.schema_validation.validate_request_data,
            self.entity_actions.read_detail,
            self.request_authorization.authorize_update_detail,
            self.entity_serializer.serialize_detail_pre_update,
            self.entity_actions.update_detail,
            self.entity_serializer.serialize_detail,
            self.post_action_hooks.update_detail_hook,
            self.response_constructor.convert_serialized_data_to_response
        ]
        return PipelineComposer(
            name=CrudActions.UPDATE_DETAIL, pipeline=update_pipeline)

    def get_create_or_update_detail_pipeline(self):
        create_or_update_detail_pipeline = [
            self.request_authentication.authenticate,
            self.request_cleaner.clean_data_for_read_detail,
            self.request_cleaner.clean_data_for_update_detail,
            self.schema_validation.validate_request_data,
            self.entity_actions.read_detail,
            self.request_authorization.authorize_update_detail,
            self.entity_serializer.serialize_detail_pre_update,
            self.entity_actions.update_detail,
            self.entity_serializer.serialize_detail,
            self.post_action_hooks.update_detail_hook,
            self.response_constructor.convert_serialized_data_to_response
        ]
        return PipelineComposer(
            name=CrudActions.CREATE_OR_UPDATE_DETAIL,
            pipeline=create_or_update_detail_pipeline
        )

    def get_read_list_pipeline(self):
        read_list_pipeline = [
            self.request_authentication.authenticate,
            self.request_params_validation.validate_request_params,
            self.request_cleaner.clean_data_for_read_list,
            self.request_authorization.add_read_list_filters,
            self.entity_actions.read_list,
            self.entity_serializer.serialize_list,
            self.post_action_hooks.read_list_hook,
            self.response_constructor.convert_serialized_data_to_response
        ]
        return PipelineComposer(
            name=CrudActions.READ_LIST, pipeline=read_list_pipeline)

    def get_create_detail_pipeline(self):
        create_detail_pipeline = [
            self.request_authentication.authenticate,
            self.request_cleaner.clean_data_for_create_detail,
            self.schema_validation.validate_request_data,
            self.request_authorization.authorize_create_detail,
            self.entity_actions.create_detail,
            self.entity_serializer.serialize_detail,
            self.post_action_hooks.create_detail_hook,
            self.response_constructor.convert_serialized_data_to_response
        ]

        return PipelineComposer(
            name=CrudActions.CREATE_DETAIL, pipeline=create_detail_pipeline)

    def delete_detail_pipeline(self):
        delete_detail_pipeline = [
            self.request_authentication.authenticate,
            self.request_cleaner.clean_data_for_delete_detail,
            self.entity_actions.read_detail,
            self.request_authorization.authorize_delete_detail,
            self.entity_actions.delete_detail,
            self.post_action_hooks.delete_detail_hook,
            self.response_constructor.convert_to_simple_response
        ]

        return PipelineComposer(
            name=CrudActions.DELETE_DETAIL, pipeline=delete_detail_pipeline)

    def get_aggregates_pipeline(self):
        aggregates_pipeline = [
            self.request_authentication.authenticate,
            self.request_params_validation.validate_request_params,
            self.request_cleaner.clean_data_for_get_aggregates,
            self.request_authorization.add_read_list_filters,
            self.entity_actions.get_aggregates,
            self.entity_serializer.serialize_entity_aggregates,
            self.post_action_hooks.get_aggregates_hook,
            self.response_constructor.convert_serialized_data_to_response
        ]

        return PipelineComposer(
            name=CrudActions.GET_AGGREGATES, pipeline=aggregates_pipeline)

