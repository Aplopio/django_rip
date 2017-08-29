import re
import uuid

from django.conf.urls import url
from django.core import urlresolvers
from http_adapter.url_types import UrlTypes
from rip.crud.crud_actions import CrudActions


class DefaultUrlReverser(object):
    def __init__(self, resource_name, url_type):
        self.url_type = url_type
        self.resource_name = resource_name

    def _get_url_name(self):
        return '{}-{}'.format(self.resource_name, self.url_type)

    def _get_list_of_value(self, value):
        return value if isinstance(value, list) else [value]

    def reverse_to_url(self, value=None):
        # url reverse can be an expensive operation in large projects.
        # todo: Find a way to cache the results
        url_name = self._get_url_name()
        if value:
            args = self._get_list_of_value(value)
        else:
            args = []
        return urlresolvers.reverse(url_name, args=args)


class CachedUrlReverser(DefaultUrlReverser):
    def __init__(self, resource_name, url_type):
        super(CachedUrlReverser, self).__init__(resource_name, url_type)
        self.url_pattern = None
        """
        ex url_pattern for detail = '/api/v1/jobs/{job_id}/resource_name/{id}'
        ex url_pattern for list = 'api/v1/jobs/{job_id}/resource_name'
        """

    def _get_url_pattern(self, list_of_value):
        """
        get the pattern of the resource url by resolving it with uuid's
        instead of actual values and cache the result.
        Use the result to string replace and get the actual url.
        For a large number of url resolutions this will greatly enhance speed
        """
        if not self.url_pattern:
            url_name = self._get_url_name()
            replace_str = uuid.uuid4().hex
            args = [replace_str for val in list_of_value]
            url_pattern = urlresolvers.reverse(url_name, args=args)
            self.url_pattern = url_pattern.replace(replace_str, '{}')
        return self.url_pattern

    def reverse_to_url(self, value=None):
        if value:
            list_of_value = self._get_list_of_value(value)
        else:
            list_of_value = []
        url_pattern = self._get_url_pattern(list_of_value)
        return url_pattern.format(*list_of_value)


class DefaultUrlGenerator(object):
    def __init__(self, url_pattern, resource_cls, trailing_slash):
        self.resource_cls = resource_cls
        self.url_pattern = url_pattern
        self.trailing_slash = trailing_slash
        # Ex url_pattern: jobs/{job_id}/apply.
        # Register function ensures Trailing / and starting / are not present
        # get job_id from the url_pattern and set it as a named parameter in
        # django url. resource_cls.dispatch function receives job_id as a kwarg.
        self.url_kwargs_regex = re.compile(r'(?<=\/\{)[^{}]*(?=\}[/]?)')
        self.url_construction_snippet = r'(?P<{url_kwarg}>[0-9a-zA-Z_-]+)'

    def _generate_url_name(self, url_type):
        """
        If you decide to override this function, make appropriate
        changes in UrlReverser as well
        """
        return '{}-{}'.format(
            self.resource_cls.get_meta().resource_name, url_type)

    def _generate_url(self, pattern, url_type):
        """
        :param pattern: Full url_pattern including /{id} if url_type=detail_url
        :param url_type: One of the values from UrlTypes
        :return: generated url
        """
        url_kwargs_list = self.url_kwargs_regex.findall(pattern)
        url_snippets = {
            url_kwarg: self.url_construction_snippet.format(
                url_kwarg=url_kwarg)
            for url_kwarg in url_kwargs_list}

        url_regex = pattern.format(**url_snippets)
        return url(url_regex, self.resource_cls.as_view(),
                   {'url_type': url_type},
                   name=self._generate_url_name(url_type))

    def get_urls(self):
        ret = []
        allowed_actions = set(self.resource_cls.get_meta().allowed_actions)

        detail_url_actions = {
            CrudActions.READ_DETAIL, CrudActions.DELETE_DETAIL,
            CrudActions.UPDATE_DETAIL, CrudActions.CREATE_OR_UPDATE_DETAIL}
        if detail_url_actions.intersection(allowed_actions):
            # detail url to be generated
            detail_url_pattern = '%s/{id}%s' % (
                self.url_pattern, self.trailing_slash)
            ret.append(
                self._generate_url(detail_url_pattern, UrlTypes.detail_url))

        list_url_actions = {CrudActions.CREATE_DETAIL, CrudActions.READ_LIST}
        if list_url_actions.intersection(allowed_actions):
            # list url to be generated
            list_url_pattern = '%s%s' % (self.url_pattern, self.trailing_slash)
            ret.append(
                self._generate_url(list_url_pattern, UrlTypes.list_url))

        if CrudActions.GET_AGGREGATES in allowed_actions:
            # aggregates url to be generated
            aggregates_url_pattern = '%s/aggregates%s' % \
                                     (self.url_pattern, self.trailing_slash)
            ret.append(self._generate_url(
                aggregates_url_pattern, UrlTypes.aggregates_url))

        return ret
