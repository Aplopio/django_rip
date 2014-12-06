class Api(object):
    def __init__(self, name, version='v1'):
        self.name = name
        self.version = version
        self.resources = {}
        self.actions = {}
        self.resources_lookup = {}

    def register_resource(self, endpoint, resource):
        if endpoint in self.resources or self.actions:
            raise AttributeError(
                '{endpoint} already registered for another resource/action'.
                format(endpoint=endpoint))
        elif endpoint.split('/')[-1] != resource.configuration['schema_cls'].\
                _meta.schema_name:
            # This is a requirement to ensure resource_uri calculation and
            # serialization of related fields works correctly.
            # TODO: come up with a better way to solve this
            raise ValueError(
                'endpoint name `{endpoint}` does match schema_name of resource'.
                format(endpoint=endpoint))
        else:
            self.resources[endpoint] = resource
            endpoint_parts = endpoint.split('/')[::2]
            self.resources_lookup["/".join(endpoint_parts)] = (
                endpoint, resource)

    def register_action(self, action):
        pass

    def resolve_resource(self, url):
        url_parts = url.split('/')[::2]
        lookup = self.resources_lookup.get("/".join(url_parts))
        return lookup[1] if lookup else None

    def resolve_endpoint(self, url):
        url_parts = url.split('/')[::2]
        lookup = self.resources_lookup.get("/".join(url_parts))
        return lookup[0] if lookup else None
