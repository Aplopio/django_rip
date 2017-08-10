import re
from django.conf.urls import url
from django_adapter.url_types import UrlTypes
from rip.crud.crud_actions import CrudActions


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
        self.url_construction_snippet = r'(?P<{url_kwarg}>[0-9a-zA-Z_]+?)'

    def _generate_url_name(self, url_type):
        return '{}-{}'.format(self.resource_cls.resource_name, url_type)

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
        allowed_actions = set(self.resource_cls.allowed_actions)

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
