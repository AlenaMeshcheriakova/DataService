from unittest.mock import patch

from sqlalchemy import select

from src.db.database import session_factory
from src.dto.schema import UserAuthTelegramDTO, UserResponse
from src.service.user_service import UserService
from tests.unit.test_data_preparation import (DataPreparation, create_test_user)
from src.model.userdb import UserDB


class TestUserService:
    """Group of Unit-Tests for class TestUserService"""

    def test_get_user_by_name(self, create_test_user):
        """
        Positive test for finding user by name
        """
        # Do tests
        test_user_name = UserService.get_user_by_name(DataPreparation.TEST_USER_NAME)

        assert test_user_name.id == DataPreparation.TEST_USER_ID
        assert test_user_name.user_name == DataPreparation.TEST_USER_NAME

    def test_get_user_by_id(self, create_test_user):
        """
        Positive test for finding user by id
        """
        # Do tests
        test_user_name = UserService.get_user_by_id(DataPreparation.TEST_USER_ID)

        assert test_user_name.id == DataPreparation.TEST_USER_ID
        assert test_user_name.user_name == DataPreparation.TEST_USER_NAME

    def test_get_user_id_by_name(self, create_test_user):
        """
        Positive test for finding user id by name
        """
        # Do tests
        test_user_id = UserService.get_user_id_by_name(DataPreparation.TEST_USER_NAME)

        assert test_user_id == DataPreparation.TEST_USER_ID

    def test_is_user_created_positive(self, create_test_user):
        """
        Positive test for finding user by name
        """
        # Do tests
        is_user_created = UserService.is_user_created(DataPreparation.TEST_USER_NAME)

        assert is_user_created is True

    def test_is_user_created_negative(self):
        """
        Negative test for finding user by name
        """
        # Do tests
        is_user_created = UserService.is_user_created(DataPreparation.TEST_USER_NAME)

        assert is_user_created is False

    @patch('src.service.user_service.AuthService.register')
    def test_create_user_by_DTO(self, mock_register):
        """
        Positive test for creating user
        """
        with patch('src.dwh.dwh_service.DwhService.send') as mock:
            mock_register.return_value = UserResponse(
                username='mock_username',
                message="mocked_message"
            )

            # Prepare data
            test_user = UserAuthTelegramDTO(
                id=DataPreparation.TEST_USER_ID,
                auth_user_id=DataPreparation.TEST_USER_AUTH_ID,
                user_name=DataPreparation.TEST_USER_NAME,
                training_length=5,
                password=DataPreparation.TEST_PASS,
                email=DataPreparation.TEST_USER_EMAIL,
                telegram_user_id=DataPreparation.TEST_TELEGRAM_USER_ID
            )

            # Do tests
            UserService.create_user_by_DTO(test_user)

            # Check results
            with session_factory() as session:
                query = select(UserDB)
                result = session.execute(query)
                res_user = result.scalars().all()
                tested_user = res_user[0]

                assert len(res_user) == 1
                assert tested_user.id == DataPreparation.TEST_USER_ID
                assert tested_user.user_name == DataPreparation.TEST_USER_NAME

    @patch('src.service.user_service.AuthService.register')
    def test_create_user_by_parameters(self, mock_register):
        """
        Positive test for creating user by parameters
        """
        with patch('src.dwh.dwh_service.DwhService.send') as mock:
            mock_register.return_value = "mocked_response"

            # Do tests
            UserService.create_user(DataPreparation.TEST_USER_NAME, DataPreparation.TEST_PASS,
                                    DataPreparation.TEST_USER_EMAIL, DataPreparation.TEST_TELEGRAM_USER_ID, 10)

            # Check results
            with session_factory() as session:
                query = select(UserDB)
                result = session.execute(query)
                res_user = result.scalars().all()
                tested_user = res_user[0]

                assert len(res_user) == 1
                assert tested_user.user_name == DataPreparation.TEST_USER_NAME
