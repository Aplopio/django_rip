from http_adapter.default_url_generator import DefaultUrlGenerator


class DefaultRouter(object):
    def __init__(self, url_prefix=None, trailing_slash='/',
                 url_generator_cls=DefaultUrlGenerator):
        self.trailing_slash = trailing_slash or ''
        self.url_generator_cls = url_generator_cls
        self.url_prefix = url_prefix or ''
        self.registry = {}
        self.name_registry = {}

    def _get_full_url_pattern(self, url_pattern):
        full_url_pattern = '{}/{}'.format(self.url_prefix, url_pattern)
        pattern_splits = [s for s in full_url_pattern.split('/') if s]
        full_url_pattern = '/'.join(pattern_splits)
        return full_url_pattern

    def register(self,  resource_cls, url_pattern=None):
        """
        :param url_pattern: Ex: 'openings', 'jobs/{job_id}/apply.
            If not provided, it defaults to the resource_name
        :param resource_cls: DjangoResource class to be
            registered at the url_pattern
        :return: None
        """
        resource_name = resource_cls.get_meta().resource_name
        url_pattern = url_pattern or resource_name

        full_url_pattern = self._get_full_url_pattern(url_pattern)
        detail_identifier_str = '{%s}' % \
                                resource_cls.get_meta().detail_identifier
        if detail_identifier_str in full_url_pattern:
            raise ValueError(
                '%s will be added to the url pattern automatically. '
                'Please provide a pattern without a %s parameter' % (
                    detail_identifier_str, detail_identifier_str))
        if full_url_pattern in self.registry:
            raise ValueError(
                "`url_pattern` {url_pattern} already registered for "
                "`resource_cls` {resource_cls}".format(
                    url_pattern=url_pattern,
                    resource_cls=resource_cls.__name__))
        if resource_name in self.name_registry:
            raise ValueError(
                "Another resource with `resource_name` {resource_name} already "
                "registered on this router".format(
                    resource_name=resource_name))
        if resource_cls in self.registry.values():
            raise ValueError(
                "`resource_cls` {resource_cls} "
                "already registered in this router".format(
                    resource_cls=resource_cls.__name__))

        if getattr(resource_cls, 'router_params', None) is not None:
            raise ValueError(
                "`resource_cls` {resource_cls} already registered on "
                "another router. A resource can be registered only once "
                "to ensure ResourceURI fields work".format(
                    resource_cls=resource_cls.__name__))

        self.registry[full_url_pattern] = resource_cls
        self.name_registry[resource_name] = resource_cls

    @property
    def urls(self):
        if not hasattr(self, '_urls'):
            self._urls = self.get_urls()
        return self._urls

    def get_urls(self):
        urls = []
        for url_pattern, resource_cls in self.registry.items():
            url_generator = self.url_generator_cls(url_pattern, resource_cls,
                                                   self.trailing_slash)
            urls.extend(url_generator.get_urls())
        return urls
