from rip.crud.decorators import validate_action
from rip.generic_steps.default_authentication import \
    DefaultAuthentication
from rip.generic_steps.default_request_params_validation import \
    DefaultRequestParamsValidation
from rip.crud.crud_actions import CrudActions
from rip.generic_steps.default_authorization import \
    DefaultAuthorization
from rip.generic_steps.default_data_cleaner import \
    DefaultRequestCleaner
from rip.generic_steps.default_entity_actions import \
    DefaultEntityActions
from rip.generic_steps.default_post_action_hooks import \
    DefaultPostActionHooks
from rip.generic_steps.default_response_converter import \
    DefaultResponseConverter
from rip.generic_steps.default_schema_serializer import \
    DefaultEntitySerializer
from rip.generic_steps.default_schema_validation import \
    DefaultSchemaValidation
from rip.crud import crud_pipeline_factory


class CrudResource(object):
    """
    Defines a Resource with CRUD actions implemented in as as series of steps
    in a pipeline
    If your resource confirms to the basic CRUD actions in Rest,
    then inherit from this class
    Usually you don't have to override methods because steps can be overridden
    in the configuration attributes

    An example:
    class Tweet(CrudResource):
    schema_cls = TweetSchema
    allowed_actions= [CrudActions.READ_LIST,
                        CrudActions.READ_DETAIL,
                        CrudActions.UPDATE_DETAIL,
                        CrudActions.CREATE_DETAIL,
                        CrudActions.DELETE_DETAIL] # list of allowed actions
    entity_actions_cls = TweetEntityActions # A mandatory hook class
                                            # that has methods for actions on
                                            #entities

    serializer_cls = TweetEntitySerializer # A hook class
                                           # for serializing entity to json

    authentication_cls = TweetAuthentication # A hook class that authenticates
                                             # a request.
                                             # Default: it checks
                                             # if a valid user is present on the
                                             # request

    authorization_cls = TweetAuthorization # A hook class
                                           # that controls access to entities
                                           # Default: there is no authorization

    allowed_filters = {'id': (EQUALS)}     # allowed filters on entity
    default_limit = 20                     # page limit for get_list
    default_offset = 0                     # default page offset for get_list

    """
    schema_cls = None
    allowed_actions = [CrudActions.READ_DETAIL, CrudActions.READ_LIST]
    filter_by_fields = {}
    order_by_fields = []
    aggregate_by_fields = []
    default_offset = 0
    default_limit = 20

    authentication_cls = DefaultAuthentication
    authorization_cls = DefaultAuthorization
    request_params_validation_cls = DefaultRequestParamsValidation
    schema_validation_cls = DefaultSchemaValidation
    data_cleaner_cls = DefaultRequestCleaner
    entity_actions_cls = DefaultEntityActions
    post_action_hooks_cls = DefaultPostActionHooks
    response_converter_cls = DefaultResponseConverter
    serializer_cls = DefaultEntitySerializer

    def _setup_configuration(self):
        """
        All steps are accepted as classes. Instantiate them with the right
        configuration and set them in a local property.
        """
        self.configuration = dict(
            schema_cls=self.schema_cls,
            allowed_actions=self.allowed_actions,
            filter_by_fields=self.filter_by_fields,
            order_by_fields=self.order_by_fields,
            aggregate_by_fields=self.aggregate_by_fields,
            default_offset=self.default_offset,
            default_limit=self.default_limit)

        authentication = self.authentication_cls(schema_cls=self.schema_cls)
        authorization = self.authorization_cls(schema_cls=self.schema_cls)
        request_params_validation = self.request_params_validation_cls(
            schema_cls=self.schema_cls,
            filter_by_fields=self.filter_by_fields,
            order_by_fields=self.order_by_fields,
            aggregate_by_fields=self.aggregate_by_fields
        )
        schema_validation = self.schema_validation_cls(
            schema_cls=self.schema_cls)
        data_cleaner = self.data_cleaner_cls(schema_cls=self.schema_cls)
        entity_actions = self.entity_actions_cls(
            schema_cls=self.schema_cls,
            default_limit=self.default_limit,
            default_offset=self.default_offset)
        post_action_hooks = self.post_action_hooks_cls(
            schema_cls=self.schema_cls)
        response_converter = self.response_converter_cls(
            schema_cls=self.schema_cls)
        serializer = self.serializer_cls(schema_cls=self.schema_cls)

        self.configuration.update(dict(
            authentication=authentication,
            authorization=authorization,
            request_params_validation=request_params_validation,
            schema_validation=schema_validation,
            data_cleaner=data_cleaner,
            entity_actions=entity_actions,
            post_action_hooks=post_action_hooks,
            response_converter=response_converter,
            serializer=serializer))

    def __new__(cls, *args, **kwargs):
        if cls.schema_cls is None:
            raise TypeError('Missing configuration property `schema_cls` \
                             on Resource `{resource_name}`'
                            .format(resource_name=cls.__name__))
        obj = super(CrudResource, cls).__new__(cls, *args, **kwargs)
        return obj

    def __init__(self):
        super(CrudResource, self).__init__()
        self._setup_configuration()

    def is_action_allowed(self, action_name):
        """
        Returns if a particular action is allowed on the resource
        as set in the allowed_actions attribute

        :param action_name:string
        :values as defined in CrudActions
        :return: bool
        """
        if action_name not in self.allowed_actions:
            return False
        return True

    @validate_action
    def read_detail(self, request):
        """
        Implements the Read Detail (read an object)

        maps to GET /api/objects/:id/ in url semantics
        :param request: rip.Request
        :return: rip.Response
        """
        pipeline = crud_pipeline_factory.read_detail_pipeline(
            configuration=self.configuration)
        return pipeline(request=request)

    @validate_action
    def update_detail(self, request):
        """
        Implements the Update Detail (partially update an object)

        maps to PATCH /api/object/:id/ in url semantics
        :param request: rip.Request
        :return: rip.Response
        """
        pipeline = crud_pipeline_factory.update_detail_pipeline(
            configuration=self.configuration)
        return pipeline(request=request)

    @validate_action
    def read_list(self, request):
        """
        Implements the List read (get a list of objects)

        maps to GET /api/objects/ in url semantics
        :param request: rip.Request
        :return: rip.Response
        """
        pipeline = crud_pipeline_factory.read_list_pipeline(
            configuration=self.configuration)
        return pipeline(request=request)

    @validate_action
    def create_detail(self, request):
        """
        Implements the Create Detail (create an object)

        maps to POST /api/objects/ in rest semantics
        :param request: rip.Request
        :return: rip.Response
        """
        pipeline = crud_pipeline_factory.create_detail_pipeline(
            configuration=self.configuration)
        return pipeline(request=request)

    @validate_action
    def delete_detail(self, request):
        """
        Implements the Delete Detail (delete an object)

        maps to DELETE /api/object_name/:id/ in url semantics
        :param request: rip.Request
        :return: rip.Response
        """
        pipeline = crud_pipeline_factory.delete_detail_pipeline(
            configuration=self.configuration)
        return pipeline(request=request)

    @validate_action
    def get_aggregates(self, request):
        """
        Implements the Get aggregates (total number of objects filtered)

        maps to PATCH /api/object_name/get_aggregates/ in url semantics
        :param request: rip.Request
        :return: rip.Response
        """
        pipeline = crud_pipeline_factory.get_aggregates_pipeline(
            configuration=self.configuration)

        return pipeline(request=request)
