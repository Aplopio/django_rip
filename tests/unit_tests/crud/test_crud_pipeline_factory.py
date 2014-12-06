import unittest

from hamcrest.core import assert_that
from hamcrest.core.core.isequal import equal_to
from mock import MagicMock
from mock import patch as mock_patch

from rip import pipeline_composer
from rip.crud.crud_actions import CrudActions
from rip.crud import crud_pipeline_factory


class TestCrudPipelineFactory(unittest.TestCase):
    @mock_patch.object(pipeline_composer, 'compose_pipeline')
    def test_read_list_pipeline_has_all_steps_in_the_right_order(self,
                                                                 compose_pipeline):
        entity_actions = MagicMock()
        entity_actions.read_list = read_list = MagicMock()
        authentication = MagicMock()
        authentication.authenticate = MagicMock()
        authorization = MagicMock()
        authorization.add_read_list_filters = add_read_list_filters = MagicMock()
        request_params_validation = MagicMock()
        request_params_validation.validate_request_params = validate_request_params = \
            MagicMock()
        cleaner = MagicMock()
        cleaner.clean_data_for_read_list = \
            clean_data_for_read_list = MagicMock()
        serializer = MagicMock()
        serializer.serialize_list = \
            serialize_list = MagicMock()
        response_converter = MagicMock()
        response_converter.convert_serialized_data_to_response = \
            convert_serialized_data_to_response = MagicMock()
        post_action_hooks = MagicMock()
        post_action_hooks.read_list_hook = read_list_hook = MagicMock()

        compose_pipeline.return_value = expected_pipeline = MagicMock()
        configuration = {
            'entity_actions': entity_actions,
            'authentication': authentication,
            'request_params_validation': request_params_validation,
            'authorization': authorization,
            'serializer': serializer,
            'data_cleaner': cleaner,
            'response_converter': response_converter,
            'post_action_hooks': post_action_hooks
        }

        pipeline = crud_pipeline_factory.read_list_pipeline(configuration)

        assert_that(pipeline, equal_to(expected_pipeline))
        compose_pipeline.assert_called_once_with(name=CrudActions.READ_LIST,
                                                 pipeline=[
                                                     authentication.authenticate,
                                                     validate_request_params,
                                                     clean_data_for_read_list,
                                                     add_read_list_filters,
                                                     read_list,
                                                     serialize_list,
                                                     read_list_hook,
                                                     convert_serialized_data_to_response
                                                 ])

    @mock_patch.object(pipeline_composer, 'compose_pipeline')
    def test_read_detail_pipeline_has_all_steps_in_the_right_order(self,
                                                                   compose_pipeline):
        entity_actions = MagicMock()
        entity_actions.read_detail = read_detail = MagicMock()
        authentication = MagicMock()
        authentication.authenticate = MagicMock()
        authorization = MagicMock()
        authorization.authorize_read_detail = authorize_read_detail = MagicMock()
        cleaner = MagicMock()
        cleaner.clean_data_for_read_detail = \
            clean_data_for_read_detail = MagicMock()
        serializer = MagicMock()
        serializer.serialize_detail = serialize_detail = MagicMock()
        response_converter = MagicMock()
        response_converter.convert_serialized_data_to_response = \
            convert_serialized_data_to_response = MagicMock()
        post_action_hooks = MagicMock()
        post_action_hooks.read_detail_hook = read_detail_hook = MagicMock()

        compose_pipeline.return_value = expected_pipeline = MagicMock()
        configuration = {
            'entity_actions': entity_actions,
            'authentication': authentication,
            'authorization': authorization,
            'serializer': serializer,
            'data_cleaner': cleaner,
            'response_converter': response_converter,
            'post_action_hooks': post_action_hooks
        }

        pipeline = crud_pipeline_factory.read_detail_pipeline(configuration)

        assert_that(pipeline, equal_to(expected_pipeline))
        compose_pipeline.assert_called_once_with(name=CrudActions.READ_DETAIL,
                                                 pipeline=[
                                                     authentication.authenticate,
                                                     clean_data_for_read_detail,
                                                     read_detail,
                                                     authorize_read_detail,
                                                     serialize_detail,
                                                     read_detail_hook,
                                                     convert_serialized_data_to_response
                                                 ])

    @mock_patch.object(pipeline_composer, 'compose_pipeline')
    def test_delete_detail_pipeline_has_all_steps_in_the_right_order(self,
                                                                     compose_pipeline):
        entity_actions = MagicMock()
        entity_actions.delete_detail = delete_detail = MagicMock()
        entity_actions.read_detail = read_detail = MagicMock()
        authentication = MagicMock()
        authentication.authenticate = MagicMock()
        authorization = MagicMock()
        authorization.authorize_delete_detail = authorize_delete_detail = MagicMock()
        cleaner = MagicMock()
        cleaner.clean_data_for_delete_detail = \
            clean_data_for_delete_detail = MagicMock()
        response_converter = MagicMock()
        post_action_hooks = MagicMock()
        post_action_hooks.delete_detail_hook = delete_detail_hook = MagicMock()
        response_converter.convert_to_simple_response= \
            convert_to_simple_response = MagicMock()

        compose_pipeline.return_value = expected_pipeline = MagicMock()
        configuration = {
            'entity_actions': entity_actions,
            'authentication': authentication,
            'authorization': authorization,
            'data_cleaner': cleaner,
            'response_converter': response_converter,
            'post_action_hooks': post_action_hooks
        }

        pipeline = crud_pipeline_factory.delete_detail_pipeline(configuration)

        assert_that(pipeline, equal_to(expected_pipeline))
        compose_pipeline.assert_called_once_with(name=CrudActions.DELETE_DETAIL,
                                                 pipeline=[
                                                     authentication.authenticate,
                                                     clean_data_for_delete_detail,
                                                     read_detail,
                                                     authorize_delete_detail,
                                                     delete_detail,
                                                     delete_detail_hook,
                                                     convert_to_simple_response
                                                 ])

    @mock_patch.object(pipeline_composer, 'compose_pipeline')
    def test_update_detail_pipeline_has_all_steps_in_the_right_order(self,
                                                                     compose_pipeline):
        entity_actions = MagicMock()
        entity_actions.read_detail = read_detail = MagicMock()
        entity_actions.update_detail = update_detail = MagicMock()
        authentication = MagicMock()
        authorization = MagicMock()
        authorization.authorize_update_detail = \
            authorize_update_detail = MagicMock()
        schema_validation = MagicMock()
        schema_validation.validate_request_data = \
            validate_request_data = MagicMock()
        schema = MagicMock()
        serializer = MagicMock()
        serializer.serialize_detail = serialize_detail = MagicMock()
        serializer.serialize_detail_pre_update = serialize_detail_pre_update = \
            MagicMock()
        data_cleaner = MagicMock()
        data_cleaner.clean_data_for_update_detail = \
            clean_data_for_update_detail = MagicMock()
        data_cleaner.clean_data_for_read_detail = \
            clean_data_for_read_detail = MagicMock()
        post_action_hooks = MagicMock()
        post_action_hooks.update_detail_hook = update_detail_hook = MagicMock()
        response_converter = MagicMock()
        response_converter.convert_serialized_data_to_response = \
            convert_serialized_data_to_response = MagicMock()

        configuration = {
            'entity_actions': entity_actions,
            'authentication': authentication,
            'authorization': authorization,
            'schema': schema,
            'schema_validation': schema_validation,
            'serializer': serializer,
            'data_cleaner': data_cleaner,
            'post_action_hooks': post_action_hooks,
            'response_converter': response_converter
        }

        compose_pipeline.return_value = expected_pipeline = MagicMock()

        pipeline = crud_pipeline_factory.update_detail_pipeline(configuration)

        assert_that(pipeline, equal_to(expected_pipeline))
        compose_pipeline.assert_called_once_with(name=CrudActions.UPDATE_DETAIL,
                                                 pipeline=[
                                                     authentication.authenticate,
                                                     clean_data_for_read_detail,
                                                     clean_data_for_update_detail,
                                                     validate_request_data,
                                                     read_detail,
                                                     authorize_update_detail,
                                                     serialize_detail_pre_update,
                                                     update_detail,
                                                     serialize_detail,
                                                     update_detail_hook,
                                                     convert_serialized_data_to_response])

    @mock_patch.object(pipeline_composer, 'compose_pipeline')
    def test_create_detail_pipeline_has_all_steps_in_the_right_order(self,
                                                                     compose_pipeline):
        entity_actions = MagicMock()
        entity_actions.create_detail = create_detail = MagicMock()
        authentication = MagicMock()
        authentication.authenticate = MagicMock()
        authorization = MagicMock()
        authorization.authorize_create_detail = \
            authorize_create_detail = MagicMock()
        schema_validation = MagicMock()
        schema_validation.validate_request_data = \
            validate_request_data = MagicMock()
        schema = MagicMock()
        serializer = MagicMock()
        serializer.serialize_detail = serialize_detail = MagicMock()
        data_cleaner = MagicMock()
        data_cleaner.clean_data_for_create_detail = \
            clean_data_for_create_detail = MagicMock()
        post_action_hooks = MagicMock()
        post_action_hooks.create_detail_hook = create_detail_hook = MagicMock()
        response_converter = MagicMock()
        response_converter.convert_serialized_data_to_response = \
            convert_serialized_data_to_response = MagicMock()

        configuration = {
            'entity_actions': entity_actions,
            'authentication': authentication,
            'authorization': authorization,
            'schema': schema,
            'schema_validation': schema_validation,
            'serializer': serializer,
            'data_cleaner': data_cleaner,
            'post_action_hooks': post_action_hooks,
            'response_converter': response_converter
        }

        compose_pipeline.return_value = expected_pipeline = MagicMock()

        pipeline = crud_pipeline_factory.create_detail_pipeline(configuration)

        assert_that(pipeline, equal_to(expected_pipeline))
        compose_pipeline.assert_called_once_with(name=CrudActions.CREATE_DETAIL,
                                                 pipeline=[
                                                     authentication.authenticate,
                                                     clean_data_for_create_detail,
                                                     validate_request_data,
                                                     authorize_create_detail,
                                                     create_detail,
                                                     serialize_detail,
                                                     create_detail_hook,
                                                     convert_serialized_data_to_response
                                                 ])



    @mock_patch.object(pipeline_composer, 'compose_pipeline')
    def test_get_aggregates_pipeline_has_all_steps_in_the_right_order(
            self, compose_pipeline):
        entity_actions = MagicMock()
        entity_actions.get_aggregates = get_aggregates = MagicMock()
        authentication = MagicMock()
        authentication.authenticate = MagicMock()
        authorization = MagicMock()
        authorization.add_read_list_filters = add_read_list_filters = MagicMock()
        request_params_validation = MagicMock()
        request_params_validation.validate_request_params = validate_request_params = \
            MagicMock()
        cleaner = MagicMock()
        cleaner.clean_data_for_get_aggregates = \
            clean_data_for_get_aggregates = MagicMock()
        serializer = MagicMock()
        serializer.serialize_entity_aggregates = \
            serialize_entity_aggregates = MagicMock()
        response_converter = MagicMock()
        response_converter.convert_serialized_data_to_response = \
            convert_serialized_data_to_response = MagicMock()
        post_action_hooks = MagicMock()
        post_action_hooks.get_aggregates_hook = get_aggregates_hook = MagicMock()

        compose_pipeline.return_value = expected_pipeline = MagicMock()
        configuration = {
            'entity_actions': entity_actions,
            'authentication': authentication,
            'request_params_validation': request_params_validation,
            'authorization': authorization,
            'serializer': serializer,
            'data_cleaner': cleaner,
            'response_converter': response_converter,
            'post_action_hooks': post_action_hooks
        }

        pipeline = crud_pipeline_factory.get_aggregates_pipeline(configuration)

        assert_that(pipeline, equal_to(expected_pipeline))
        compose_pipeline.assert_called_once_with(name=CrudActions.GET_AGGREGATES,
                                                 pipeline=[
                                                     authentication.authenticate,
                                                     validate_request_params,
                                                     clean_data_for_get_aggregates,
                                                     add_read_list_filters,
                                                     get_aggregates,
                                                     serialize_entity_aggregates,
                                                     get_aggregates_hook,
                                                     convert_serialized_data_to_response
                                                 ])
