from sqlalchemy import select

from src.db.database import session_factory
from src.dto.schema import UserCreateTelegramDTO
from src.service.user_service import UserService
from tests.unit.test_data_preparation import (DataPreparation, create_test_user)
from userdb import UserDB


class TestUserService:
    """Group of Unit-Tests for class TestUserService"""

    def test_get_user_by_name(self, create_test_user):
        """
        Positive test for finding user by name
        """
        # Do tests
        test_user_name = UserService.get_user_by_name(DataPreparation.TEST_USER_NAME)

        assert test_user_name.id == DataPreparation.TEST_USER_ID
        assert test_user_name.telegram_user_id == str(DataPreparation.TEST_TELEGRAM_USER_ID)
        assert test_user_name.user_name == DataPreparation.TEST_USER_NAME
        assert test_user_name.email == DataPreparation.TEST_USER_EMAIL

    def test_get_user_by_id(self, create_test_user):
        """
        Positive test for finding user by id
        """
        # Do tests
        test_user_name = UserService.get_user_by_id(DataPreparation.TEST_USER_ID)

        assert test_user_name.id == DataPreparation.TEST_USER_ID
        assert test_user_name.telegram_user_id == str(DataPreparation.TEST_TELEGRAM_USER_ID)
        assert test_user_name.user_name == DataPreparation.TEST_USER_NAME
        assert test_user_name.email == DataPreparation.TEST_USER_EMAIL

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

    def test_create_user_by_DTO(self):
        """
        Positive test for creating user
        """
        # Prepare data
        test_user = UserCreateTelegramDTO(
            id=DataPreparation.TEST_USER_ID,
            user_name=DataPreparation.TEST_USER_NAME,
            telegram_user_id=DataPreparation.TEST_TELEGRAM_USER_ID,
            training_length=5,
            hashed_password=DataPreparation.TEST_PASS,
            email=DataPreparation.TEST_USER_EMAIL,
            is_active=True
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
            assert tested_user.telegram_user_id == str(DataPreparation.TEST_TELEGRAM_USER_ID)
            assert tested_user.user_name == DataPreparation.TEST_USER_NAME
            assert tested_user.email == DataPreparation.TEST_USER_EMAIL

    def test_create_user_by_parameters(self):
        """
        Positive test for creating user by parameters
        """
        # Do tests
        UserService.create_user(DataPreparation.TEST_USER_NAME, DataPreparation.TEST_USER_EMAIL,
                                DataPreparation.TEST_PASS, DataPreparation.TEST_TELEGRAM_USER_ID, 10)

        # Check results
        with session_factory() as session:
            query = select(UserDB)
            result = session.execute(query)
            res_user = result.scalars().all()
            tested_user = res_user[0]

            assert len(res_user) == 1
            assert tested_user.telegram_user_id == str(DataPreparation.TEST_TELEGRAM_USER_ID)
            assert tested_user.user_name == DataPreparation.TEST_USER_NAME
            assert tested_user.email == DataPreparation.TEST_USER_EMAIL
            assert tested_user.hashed_password == DataPreparation.TEST_PASS
