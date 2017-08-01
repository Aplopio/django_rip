import unittest

from hamcrest.core import assert_that
from hamcrest.core.core.isequal import equal_to
from mock import MagicMock
from mock import patch as mock_patch

from rip.crud import pipeline_composer, crud_pipelines
from rip.crud.crud_actions import CrudActions
from rip.crud.crud_pipelines import PipelineConfig


class TestCrudPipelineFactory(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCrudPipelineFactory, self).__init__(*args, **kwargs)
        configuration = MagicMock()
        configuration.schema_cls = self.schema_cls = MagicMock()

        configuration.entity_actions = MagicMock()
        configuration.entity_actions.read_list = self.read_list = MagicMock()
        configuration.entity_actions.read_detail = self.read_detail = MagicMock()
        configuration.entity_actions.delete_detail = self.delete_detail = MagicMock()
        configuration.entity_actions.update_detail = self.update_detail = MagicMock()
        configuration.entity_actions.create_detail = self.create_detail = MagicMock()
        configuration.entity_actions.get_aggregates = self.get_aggregates = MagicMock()

        configuration.authentication = MagicMock()
        configuration.authentication.authenticate = self.authenticate = MagicMock()

        configuration.authorization = MagicMock()
        configuration.authorization \
            .add_read_list_filters = self.add_read_list_filters = MagicMock()
        configuration.authorization.authorize_read_detail = \
            self.authorize_read_detail = MagicMock()
        configuration.authorization \
            .authorize_delete_detail = self.authorize_delete_detail = MagicMock()
        configuration.authorization.authorize_update_detail = \
            self.authorize_update_detail = MagicMock()
        configuration.authorization.authorize_create_detail = \
            self.authorize_create_detail = MagicMock()

        configuration.schema_validation = MagicMock()
        configuration.schema_validation.validate_request_data = \
            self.validate_request_data = MagicMock()

        configuration.request_params_validation = MagicMock()
        configuration.request_params_validation \
            .validate_request_params = self.validate_request_params = \
            MagicMock()

        configuration.data_cleaner = MagicMock()
        configuration.data_cleaner.clean_data_for_read_list = \
            self.clean_data_for_read_list = MagicMock()
        configuration.data_cleaner.clean_data_for_read_detail = \
            self.clean_data_for_read_detail = MagicMock()
        configuration.data_cleaner.clean_data_for_delete_detail = \
            self.clean_data_for_delete_detail = MagicMock()
        configuration.data_cleaner.clean_data_for_update_detail = \
            self.clean_data_for_update_detail = MagicMock()
        configuration.data_cleaner.clean_data_for_create_detail = \
            self.clean_data_for_create_detail = MagicMock()
        configuration.data_cleaner.clean_data_for_get_aggregates = \
            self.clean_data_for_get_aggregates = MagicMock()

        configuration.serializer = MagicMock()
        configuration.serializer.serialize_list = \
            self.serialize_list = MagicMock()
        configuration.serializer.serialize_detail = self.serialize_detail = MagicMock()
        configuration.serializer.serialize_detail_pre_update = \
            self.serialize_detail_pre_update = MagicMock()
        configuration.serializer.serialize_entity_aggregates = \
            self.serialize_entity_aggregates = MagicMock()

        configuration.response_converter = MagicMock()
        configuration.response_converter.convert_serialized_data_to_response = \
            self.convert_serialized_data_to_response = MagicMock()
        configuration.response_converter.convert_to_simple_response = \
            self.convert_to_simple_response = MagicMock()

        configuration.post_action_hooks = MagicMock()
        configuration.post_action_hooks.read_list_hook = self.read_list_hook = \
            MagicMock()
        configuration.post_action_hooks.read_detail_hook = \
            self.read_detail_hook = MagicMock()
        configuration.post_action_hooks.delete_detail_hook = \
            self.delete_detail_hook = MagicMock()
        configuration.post_action_hooks.update_detail_hook = \
            self.update_detail_hook = MagicMock()
        configuration.post_action_hooks.create_detail_hook = \
            self.create_detail_hook = MagicMock()
        configuration.post_action_hooks \
            .get_aggregates_hook = self.get_aggregates_hook = MagicMock()

        self.configuration = configuration


    @mock_patch.object(pipeline_composer, 'compose_pipeline')
    def test_read_list_pipeline_has_all_steps_in_the_right_order(
            self,
            compose_pipeline):
        configuration = self.configuration
        compose_pipeline.return_value = expected_pipeline = MagicMock()

        pipeline = crud_pipelines.read_list_pipeline(configuration)

        assert_that(pipeline, equal_to(expected_pipeline))
        compose_pipeline.assert_called_once_with(
            name=CrudActions.READ_LIST,
            pipeline=[
                self.authenticate,
                self.validate_request_params,
                self.clean_data_for_read_list,
                self.add_read_list_filters,
                self.read_list,
                self.serialize_list,
                self.read_list_hook,
                self.convert_serialized_data_to_response
            ])

    @mock_patch.object(pipeline_composer, 'compose_pipeline')
    def test_read_detail_pipeline_has_all_steps_in_the_right_order(
            self,
            compose_pipeline):

        configuration = self.configuration
        compose_pipeline.return_value = expected_pipeline = MagicMock()
        pipeline = crud_pipelines.read_detail_pipeline(configuration)
        assert_that(pipeline, equal_to(expected_pipeline))
        compose_pipeline.assert_called_once_with(
            name=CrudActions.READ_DETAIL,
            pipeline=[
                self.authenticate,
                self.clean_data_for_read_detail,
                self.read_detail,
                self.authorize_read_detail,
                self.serialize_detail,
                self.read_detail_hook,
                self.convert_serialized_data_to_response
            ])

    @mock_patch.object(pipeline_composer, 'compose_pipeline')
    def test_delete_detail_pipeline_has_all_steps_in_the_right_order(
            self,
            compose_pipeline):

        compose_pipeline.return_value = expected_pipeline = MagicMock()
        configuration = self.configuration

        pipeline = crud_pipelines.delete_detail_pipeline(configuration)

        assert_that(pipeline, equal_to(expected_pipeline))
        compose_pipeline.assert_called_once_with(
            name=CrudActions.DELETE_DETAIL,
            pipeline=[
                self.authenticate,
                self.clean_data_for_delete_detail,
                self.read_detail,
                self.authorize_delete_detail,
                self.delete_detail,
                self.delete_detail_hook,
                self.convert_to_simple_response
            ])

    @mock_patch.object(pipeline_composer, 'compose_pipeline')
    def test_update_detail_pipeline_has_all_steps_in_the_right_order(
            self,
            compose_pipeline):

        configuration = self.configuration
        compose_pipeline.return_value = expected_pipeline = MagicMock()

        pipeline = crud_pipelines.update_detail_pipeline(configuration)

        assert_that(pipeline, equal_to(expected_pipeline))
        compose_pipeline.assert_called_once_with(
            name=CrudActions.UPDATE_DETAIL,
            pipeline=[
                self.authenticate,
                self.clean_data_for_read_detail,
                self.clean_data_for_update_detail,
                self.validate_request_data,
                self.read_detail,
                self.authorize_update_detail,
                self.serialize_detail_pre_update,
                self.update_detail,
                self.serialize_detail,
                self.update_detail_hook,
                self.convert_serialized_data_to_response])

    @mock_patch.object(pipeline_composer, 'compose_pipeline')
    def test_create_or_update_detail_pipeline_has_all_steps_in_the_right_order(
            self,
            compose_pipeline):

        configuration = self.configuration
        compose_pipeline.return_value = expected_pipeline = MagicMock()

        pipeline = crud_pipelines.create_or_update_detail_pipeline(configuration)

        assert_that(pipeline, equal_to(expected_pipeline))
        compose_pipeline.assert_called_once_with(
            name=CrudActions.CREATE_OR_UPDATE_DETAIL,
            pipeline=[
                self.authenticate,
                self.clean_data_for_read_detail,
                self.clean_data_for_update_detail,
                self.validate_request_data,
                self.read_detail,
                self.authorize_update_detail,
                self.serialize_detail_pre_update,
                self.update_detail,
                self.serialize_detail,
                self.update_detail_hook,
                self.convert_serialized_data_to_response])

    @mock_patch.object(pipeline_composer, 'compose_pipeline')
    def test_create_detail_pipeline_has_all_steps_in_the_right_order(
            self,
            compose_pipeline):

        configuration = self.configuration
        compose_pipeline.return_value = expected_pipeline = MagicMock()

        pipeline = crud_pipelines.create_detail_pipeline(configuration)

        assert_that(pipeline, equal_to(expected_pipeline))
        compose_pipeline.assert_called_once_with(
            name=CrudActions.CREATE_DETAIL,
            pipeline=[
                self.authenticate,
                self.clean_data_for_create_detail,
                self.validate_request_data,
                self.authorize_create_detail,
                self.create_detail,
                self.serialize_detail,
                self.create_detail_hook,
                self.convert_serialized_data_to_response
            ])

    @mock_patch.object(pipeline_composer, 'compose_pipeline')
    def test_get_aggregates_pipeline_has_all_steps_in_the_right_order(
            self, compose_pipeline):

        compose_pipeline.return_value = expected_pipeline = MagicMock()
        configuration = self.configuration

        pipeline = crud_pipelines.get_aggregates_pipeline(configuration)

        assert_that(pipeline, equal_to(expected_pipeline))
        compose_pipeline.assert_called_once_with(
            name=CrudActions.GET_AGGREGATES,
            pipeline=[
                self.authenticate,
                self.validate_request_params,
                self.clean_data_for_get_aggregates,
                self.add_read_list_filters,
                self.get_aggregates,
                self.serialize_entity_aggregates,
                self.get_aggregates_hook,
                self.convert_serialized_data_to_response
            ])
