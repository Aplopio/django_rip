from rip.default_view_actions import DefaultViewActions
from rip.generic_steps.default_authentication import \
    DefaultAuthentication
from rip.generic_steps.default_post_action_hooks import \
    DefaultPostActionHooks
from rip.generic_steps.default_response_converter import \
    DefaultResponseConverter
from rip.generic_steps.default_schema_serializer import \
    DefaultEntitySerializer
from rip.generic_steps.default_schema_validation import \
    DefaultSchemaValidation
from rip.view import view_pipeline_factory
from rip.view.decorators import validate_view_action
from rip.view.default_view_authorization import DefaultViewAuthorization
from rip.view.view_actions import ViewActions


class ViewResource(object):
    """
    Defines a View Resource which like a plain old django view that returns a json.
    Additionally get options to override authentication, authorization

    Usually you don't have to override methods because steps can be overridden
    in the configuration attributes

    An example:
    class Tweet(ViewResource):
    schema_cls = TweetSchema
    allowed_actions= [ViewActions.read] # list of allowed actions
    view_actions_cls = TweetEntityActions # A mandatory hook class
                                            # that has methods for actions on
                                            # for the actual view logic

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
    """
    schema_cls = None
    allowed_actions = [ViewActions.READ]
    filter_by_fields = {}

    authentication_cls = DefaultAuthentication
    authorization_cls = DefaultViewAuthorization
    schema_validation_cls = DefaultSchemaValidation
    view_actions_cls = DefaultViewActions
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
            filter_by_fields=self.filter_by_fields)

        authentication = self.authentication_cls(schema_cls=self.schema_cls)
        authorization = self.authorization_cls()
        schema_validation = self.schema_validation_cls(
            schema_cls=self.schema_cls)
        view_actions = self.view_actions_cls()
        post_action_hooks = self.post_action_hooks_cls(
            schema_cls=self.schema_cls)
        response_converter = self.response_converter_cls(
            schema_cls=self.schema_cls)
        serializer = self.serializer_cls(schema_cls=self.schema_cls)

        self.configuration.update(dict(
            authentication=authentication,
            authorization=authorization,
            schema_validation=schema_validation,
            view_actions=view_actions,
            post_action_hooks=post_action_hooks,
            response_converter=response_converter,
            serializer=serializer))

    def __new__(cls, *args, **kwargs):
        if cls.schema_cls is None:
            raise TypeError('Missing configuration property `schema_cls` \
                             on Resource `{resource_name}`'
                            .format(resource_name=cls.__name__))
        obj = super(ViewResource, cls).__new__(cls, *args, **kwargs)
        return obj

    def __init__(self):
        super(ViewResource, self).__init__()
        self._setup_configuration()

    def is_action_allowed(self, action_name):
        """
        Returns if a particular action is allowed on the resource
        as set in the allowed_actions attribute

        :param action_name:string
        :values as defined in ViewActions
        :return: bool
        """
        if action_name not in self.allowed_actions:
            return False
        return True

    @validate_view_action
    def read(self, request):
        """
        Implements HTTP GET
        :param request: rip.Request
        :return: rip.Response
        """
        pipeline = view_pipeline_factory.read_pipeline(
            configuration=self.configuration)
        return pipeline(request=request)
