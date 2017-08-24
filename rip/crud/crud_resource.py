from functools import partial

from rip.crud.crud_actions import CrudActions
from rip.crud.pipeline_composer import PipelineComposer
from rip.crud.resource_schema_mixin import ResourceSchemaMixin
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


class CrudResource(ResourceSchemaMixin):
    """
    Defines a Resource with CRUD actions implemented in as as series of steps
    in a pipeline
    If you want basic CRUD actions in Rest then inherit from this class
    """

    # Field definitions go here.
    # field1 = IntegerField()
    # field2 = CharField()
    # ...

    class Meta:  # configuration of params for the resource
        resource_name = None
        # allow only read actions by default to avoid unintended errors
        allowed_actions = [CrudActions.READ_DETAIL, CrudActions.READ_LIST]
        filter_by_fields = {}
        order_by_fields = []
        aggregate_by_fields = []
        default_offset = 0
        default_limit = 20

        request_authentication_cls = DefaultAuthentication
        request_authorization_cls = DefaultAuthorization
        request_params_validation_cls = DefaultRequestParamsValidation
        schema_validation_cls = DefaultSchemaValidation
        request_cleaner_cls = DefaultRequestCleaner
        entity_actions_cls = DefaultEntityActions
        entity_serializer_cls = DefaultEntitySerializer
        post_action_hooks_cls = DefaultPostActionHooks
        response_constructor_cls = DefaultResponseConstructor

    def __init__(self):
        super(CrudResource, self).__init__()

        self.request_authentication = self.get_request_authentication()
        self.request_authorization = self.get_request_authorization()
        self.request_params_validation = self.get_request_params_validation()
        self.schema_validation = self.get_schema_validation()
        self.request_cleaner = self.get_request_cleaner()
        self.entity_actions = self.get_entity_actions()
        self.entity_serializer = self.get_entity_serializer()
        self.post_action_hooks = self.get_post_action_hooks()
        self.response_constructor = self.get_response_constructor()

        self.pipelines = {
            CrudActions.READ_DETAIL: self.get_read_detail_pipeline(),
            CrudActions.UPDATE_DETAIL: self.get_update_detail_pipeline(),
            CrudActions.READ_LIST: self.get_read_list_pipeline(),
            CrudActions.CREATE_DETAIL: self.get_create_detail_pipeline(),
            CrudActions.CREATE_OR_UPDATE_DETAIL:
                self.get_create_or_update_detail_pipeline(),
            CrudActions.GET_AGGREGATES: self.get_aggregates_pipeline(),
            CrudActions.DELETE_DETAIL: self.get_delete_detail_pipeline()
        }

    def run_crud_action(self, action_name, request):
        if action_name not in self.get_meta().allowed_actions:
            return Response(
                is_success=False, reason=error_types.MethodNotAllowed)
        request.context_params['crud_action'] = action_name
        crud_pipeline = self.pipelines[action_name]
        return crud_pipeline(request)

    def get_request_authentication(self):
        return self.get_meta().request_authentication_cls(resource=self)

    def get_request_authorization(self):
        return self.get_meta().request_authorization_cls(resource=self)

    def get_request_params_validation(self):
        return self.get_meta().request_params_validation_cls(resource=self)

    def get_schema_validation(self):
        return self.get_meta().schema_validation_cls(resource=self)

    def get_request_cleaner(self):
        return self.get_meta().request_cleaner_cls(resource=self)

    def get_entity_actions(self):
        return self.get_meta().entity_actions_cls(resource=self)

    def get_entity_serializer(self):
        return self.get_meta().entity_serializer_cls(resource=self)

    def get_post_action_hooks(self):
        return self.get_meta().post_action_hooks_cls(resource=self)

    def get_response_constructor(self):
        return self.get_meta().response_constructor_cls(resource=self)

    def get_read_detail_pipeline(self):
        read_detail_pipeline = [
            self.request_authentication.authenticate,
            self.request_cleaner.clean_data_for_read_detail,
            partial(self.entity_actions.read_detail,
                    get_entity_fn=getattr(self, 'get_entity', None)),
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
            partial(self.entity_actions.read_detail,
                    get_entity_fn=getattr(self, 'get_entity', None)),
            self.request_authorization.authorize_update_detail,
            self.entity_serializer.serialize_detail_pre_update,
            partial(self.entity_actions.update_detail,
                    update_entity_fn=getattr(self, 'update_entity', None)),
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
            partial(self.entity_actions.read_detail,
                    get_entity_fn=getattr(self, 'get_entity', None)),
            self.request_authorization.authorize_update_detail,
            self.entity_serializer.serialize_detail_pre_update,
            partial(self.entity_actions.update_detail,
                    update_entity_fn=getattr(self, 'update_entity', None)),
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
            partial(self.entity_actions.read_list,
                    get_entity_list_fn=getattr(self, 'get_entity_list', None),
                    get_total_count_fn=getattr(self, 'get_total_count', None)),
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
            partial(self.entity_actions.create_detail,
                    create_entity_fn=getattr(self, 'create_entity', None)),
            self.entity_serializer.serialize_detail,
            self.post_action_hooks.create_detail_hook,
            self.response_constructor.convert_serialized_data_to_response
        ]

        return PipelineComposer(
            name=CrudActions.CREATE_DETAIL, pipeline=create_detail_pipeline)

    def get_delete_detail_pipeline(self):
        delete_detail_pipeline = [
            self.request_authentication.authenticate,
            self.request_cleaner.clean_data_for_delete_detail,
            partial(self.entity_actions.read_detail,
                    get_entity_fn=getattr(self, 'get_entity', None)),
            self.request_authorization.authorize_delete_detail,
            partial(self.entity_actions.delete_detail,
                    delete_entity_fn=getattr(self, 'delete_entity', None)),
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
            partial(self.entity_actions.get_aggregates,
                    get_aggregates_fn=getattr(self, 'get_aggregates', None)),
            self.entity_serializer.serialize_entity_aggregates,
            self.post_action_hooks.get_aggregates_hook,
            self.response_constructor.convert_serialized_data_to_response
        ]

        return PipelineComposer(
            name=CrudActions.GET_AGGREGATES, pipeline=aggregates_pipeline)
