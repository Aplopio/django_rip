import unittest

from mock import MagicMock

from rip.crud.crud_resource import CrudResource
from rip.generic_steps import filter_operators
from rip.generic_steps.default_request_params_validation import \
    DefaultRequestParamsValidation
from rip.schema_fields.string_field import StringField


class TestEntityActionsReadDetail(unittest.TestCase):

    def setUp(self):

        class TestResource(CrudResource):
            f1 = StringField()

            class Meta:
                filter_by_fields = {'f1': (filter_operators.EQUALS,
                                           filter_operators.GT)}

        self.request_params_validator = DefaultRequestParamsValidation(
            resource=TestResource())

    def test_should_fail_for_unallowed_filter_type(self):
        request = MagicMock()
        request.context_params = dict(request_filters={'f1__in': 1})

        response = self.request_params_validator.validate_request_params(
            request)

        assert not response.is_success
