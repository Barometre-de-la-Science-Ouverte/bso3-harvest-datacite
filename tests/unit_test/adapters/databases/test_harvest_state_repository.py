from unittest import TestCase

from adapters.databases.harvest_state_repository import HarvestStateRepository
from tests.unit_test.adapters.databases.mock_postgres_session import MockPostgresSession

TESTED_MODULE = "adapters.databases.harvest_state_repository"


class TestHarvestStateRepository(TestCase):
    def setUp(self):
        # Given
        host: str = "fake_host"
        port: int = 0
        username: str = "fake_username"
        password: str = "fake_password"
        database_name: str = "fake_db_name"

        self.mock_postgres_session = MockPostgresSession(host, port, username, password, database_name)

        self.harvest_state_repository = HarvestStateRepository(self.mock_postgres_session)

    def test_given_mock_postgres_session_and_a_harvest_state_repository_when_using_get_without_filter_then_all_methods_of_the_repository_are_called_once_except_getEngine_called_0_time(self):
        # Given after setUp
        nb_calls_init_expected: int = 1
        nb_calls_getEngine_expected: int = 0
        nb_calls_getSession_expected: int = 1
        nb_calls_sessionScope_expected: int = 1

        # When
        self.harvest_state_repository.get()

        # Then
        assert self.mock_postgres_session.nb_calls_init == nb_calls_init_expected
        assert self.mock_postgres_session.nb_calls_getEngine == nb_calls_getEngine_expected
        assert self.mock_postgres_session.nb_calls_getSession == nb_calls_getSession_expected
        assert self.mock_postgres_session.nb_calls_sessionScope == nb_calls_sessionScope_expected

    def test_given_mock_postgres_session_and_a_harvest_state_repository_when_using_get_with_right_filter_then_all_methods_of_the_repository_are_called_once_except_getEngine_called_0_time(self):
        # Given after setUp
        nb_calls_init_expected: int = 1
        nb_calls_getEngine_expected: int = 0
        nb_calls_getSession_expected: int = 1
        nb_calls_sessionScope_expected: int = 1

        filter_args: dict = {"id": 1}

        # When
        self.harvest_state_repository.get(filter_args)

        # Then
        assert self.mock_postgres_session.nb_calls_init == nb_calls_init_expected
        assert self.mock_postgres_session.nb_calls_getEngine == nb_calls_getEngine_expected
        assert self.mock_postgres_session.nb_calls_getSession == nb_calls_getSession_expected
        assert self.mock_postgres_session.nb_calls_sessionScope == nb_calls_sessionScope_expected

    def test_given_mock_postgres_session_and_a_harvest_state_repository_when_using_get_with_wrong_name_element_in_filter_then_raise_exception(
        self,
    ):
        # Given after setUp
        nb_calls_init_expected: int = 1
        nb_calls_getEngine_expected: int = 0
        nb_calls_getSession_expected: int = 0
        nb_calls_sessionScope_expected: int = 0

        filter_args: dict = {"wrong_name": 1}

        exception_msg_expected: str = "Element not available in 'HarvestStateTable' : 'wrong_name'"

        # When
        with self.assertRaises(Exception) as context:
            self.harvest_state_repository.get(filter_args)

        self.assertTrue(exception_msg_expected in str(context.exception))

        # Then
        assert self.mock_postgres_session.nb_calls_init == nb_calls_init_expected
        assert self.mock_postgres_session.nb_calls_getEngine == nb_calls_getEngine_expected
        assert self.mock_postgres_session.nb_calls_getSession == nb_calls_getSession_expected
        assert self.mock_postgres_session.nb_calls_sessionScope == nb_calls_sessionScope_expected

    def test_given_mock_postgres_session_and_a_harvest_state_repository_when_using_get_with_wrong_type_element_in_filter_then_raise_exception(
        self,
    ):
        # Given after setUp
        nb_calls_init_expected: int = 1
        nb_calls_getEngine_expected: int = 0
        nb_calls_getSession_expected: int = 0
        nb_calls_sessionScope_expected: int = 0

        filter_args: dict = {"id": "wrong_type"}

        exception_msg_expected: str = "Element type not correct for 'HarvestStateTable' : got '<class 'str'>' and expected '<class 'int'>' for 'id' attribute"

        # When
        with self.assertRaises(Exception) as context:
            self.harvest_state_repository.get(filter_args)

        self.assertTrue(exception_msg_expected in str(context.exception))

        # Then
        assert self.mock_postgres_session.nb_calls_init == nb_calls_init_expected
        assert self.mock_postgres_session.nb_calls_getEngine == nb_calls_getEngine_expected
        assert self.mock_postgres_session.nb_calls_getSession == nb_calls_getSession_expected
        assert self.mock_postgres_session.nb_calls_sessionScope == nb_calls_sessionScope_expected

    def test_given_mock_postgres_session_and_a_repository_when_using_update_from_repository_with_empty_arg_dict_then_all_methods_of_repository_are_called_once_except_getEngine_called_0_time(self):
        # Given after setUp
        nb_calls_init_expected: int = 1
        nb_calls_getEngine_expected: int = 0
        nb_calls_getSession_expected: int = 1
        nb_calls_sessionScope_expected: int = 1

        elements_to_update: dict = {}

        # When
        self.harvest_state_repository.update(elements_to_update)

        # Then
        assert self.mock_postgres_session.nb_calls_init == nb_calls_init_expected
        assert self.mock_postgres_session.nb_calls_getEngine == nb_calls_getEngine_expected
        assert self.mock_postgres_session.nb_calls_getSession == nb_calls_getSession_expected
        assert self.mock_postgres_session.nb_calls_sessionScope == nb_calls_sessionScope_expected

    def test_given_mock_postgres_session_and_a_repository_when_using_update_from_repository_with_not_empty_arg_dict_then_all_methods_of_repository_are_called_once_except_getEngine_called_0_time(self):
        # Given after setUp
        nb_calls_init_expected: int = 1
        nb_calls_getEngine_expected: int = 0
        nb_calls_getSession_expected: int = 1
        nb_calls_sessionScope_expected: int = 1

        elements_to_update: dict = {"number_missed": 0}

        # When
        self.harvest_state_repository.update(elements_to_update)

        # Then
        assert self.mock_postgres_session.nb_calls_init == nb_calls_init_expected
        assert self.mock_postgres_session.nb_calls_getEngine == nb_calls_getEngine_expected
        assert self.mock_postgres_session.nb_calls_getSession == nb_calls_getSession_expected
        assert self.mock_postgres_session.nb_calls_sessionScope == nb_calls_sessionScope_expected

    def test_given_mock_postgres_session_and_a_harvest_state_repository_when_using_update_from_repository_with_wrong_element_in_dict_arg_then_raise_specific_exception(self):
        # Given after setUp
        nb_calls_init_expected: int = 1
        nb_calls_getEngine_expected: int = 0
        nb_calls_getSession_expected: int = 0
        nb_calls_sessionScope_expected: int = 0

        elements_to_update: dict = {"key_nonexistant": "value"}

        exception_msg_expected: str = "Element not available in 'HarvestStateTable' : 'key_nonexistant'"

        # When
        with self.assertRaises(Exception) as context:
            self.harvest_state_repository.update(elements_to_update)

        self.assertTrue(exception_msg_expected in str(context.exception))

        # Then
        assert self.mock_postgres_session.nb_calls_init == nb_calls_init_expected
        assert self.mock_postgres_session.nb_calls_getEngine == nb_calls_getEngine_expected
        assert self.mock_postgres_session.nb_calls_getSession == nb_calls_getSession_expected
        assert self.mock_postgres_session.nb_calls_sessionScope == nb_calls_sessionScope_expected

    def test_given_mock_postgres_session_and_a_harvest_state_repository_when_using_update_from_repository_with_wrong_type_element_in_dict_arg_then_raise_specific_exception(self):
        # Given after setUp
        nb_calls_init_expected: int = 1
        nb_calls_getEngine_expected: int = 0
        nb_calls_getSession_expected: int = 0
        nb_calls_sessionScope_expected: int = 0

        elements_to_update: dict = {"start_date": "toto"}

        exception_msg_expected: str = "Element type not correct for 'HarvestStateTable' : got '<class 'str'>' and expected '<class 'datetime.datetime'>' for 'start_date' attribute"

        # When
        with self.assertRaises(Exception) as context:
            self.harvest_state_repository.update(elements_to_update)

        self.assertTrue(exception_msg_expected in str(context.exception))

        # Then
        assert self.mock_postgres_session.nb_calls_init == nb_calls_init_expected
        assert self.mock_postgres_session.nb_calls_getEngine == nb_calls_getEngine_expected
        assert self.mock_postgres_session.nb_calls_getSession == nb_calls_getSession_expected
        assert self.mock_postgres_session.nb_calls_sessionScope == nb_calls_sessionScope_expected

    def test_given_mock_postgres_session_and_a_harvest_state_repository_when_using_update_from_repository_with_wrong_type_element_in_filter_then_raise_specific_exception(self):
        # Given after setUp
        nb_calls_init_expected: int = 1
        nb_calls_getEngine_expected: int = 0
        nb_calls_getSession_expected: int = 0
        nb_calls_sessionScope_expected: int = 0

        filter: dict = {"start_date": "toto"}

        exception_msg_expected: str = "Element type not correct for 'HarvestStateTable' : got '<class 'str'>' and expected '<class 'datetime.datetime'>' for 'start_date' attribute"

        # When
        with self.assertRaises(Exception) as context:
            self.harvest_state_repository.update({}, filter)

        self.assertTrue(exception_msg_expected in str(context.exception))

        # Then
        assert self.mock_postgres_session.nb_calls_init == nb_calls_init_expected
        assert self.mock_postgres_session.nb_calls_getEngine == nb_calls_getEngine_expected
        assert self.mock_postgres_session.nb_calls_getSession == nb_calls_getSession_expected
        assert self.mock_postgres_session.nb_calls_sessionScope == nb_calls_sessionScope_expected

    def test_given_mock_postgres_session_and_a_harvest_state_repository_when_using_update_from_repository_with_wrong_element_in_filter_arg_then_raise_specific_exception(self):
        # Given after setUp
        nb_calls_init_expected: int = 1
        nb_calls_getEngine_expected: int = 0
        nb_calls_getSession_expected: int = 0
        nb_calls_sessionScope_expected: int = 0

        filter: dict = {"key_nonexistant": "value"}

        exception_msg_expected: str = "Element not available in 'HarvestStateTable' : 'key_nonexistant'"

        # When
        with self.assertRaises(Exception) as context:
            self.harvest_state_repository.update({}, filter)

        self.assertTrue(exception_msg_expected in str(context.exception))

        # Then
        assert self.mock_postgres_session.nb_calls_init == nb_calls_init_expected
        assert self.mock_postgres_session.nb_calls_getEngine == nb_calls_getEngine_expected
        assert self.mock_postgres_session.nb_calls_getSession == nb_calls_getSession_expected
        assert self.mock_postgres_session.nb_calls_sessionScope == nb_calls_sessionScope_expected
