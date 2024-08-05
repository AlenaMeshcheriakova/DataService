from sqlalchemy import select

from src.data.user_orm import UserOrm
from src.db.database import session_factory
from src.dto.schema import UserCreateTelegramDTO
from tests.unit.test_data_preparation import (DataPreparation, create_test_user)
from userdb import UserDB


class TestUserOrm:
    """Group of Unit-Tests for class UserOrm"""

    def test_find_user_by_name(self, create_test_user):
        """
        Positive test for finding user by name
        """
        # Do tests
        test_user_name = UserOrm.find_user_by_name(DataPreparation.TEST_USER_NAME)

        assert test_user_name.id == DataPreparation.TEST_USER_ID
        assert test_user_name.telegram_user_id == str(DataPreparation.TEST_TELEGRAM_USER_ID)
        assert test_user_name.user_name == DataPreparation.TEST_USER_NAME
        assert test_user_name.email == DataPreparation.TEST_USER_EMAIL

    def test_find_user_by_id(self, create_test_user):
        """
        Positive test for finding user by id
        """
        # Do tests
        test_user_name = UserOrm.find_user_by_id(DataPreparation.TEST_USER_ID)

        assert test_user_name.id == DataPreparation.TEST_USER_ID
        assert test_user_name.telegram_user_id == str(DataPreparation.TEST_TELEGRAM_USER_ID)
        assert test_user_name.user_name == DataPreparation.TEST_USER_NAME
        assert test_user_name.email == DataPreparation.TEST_USER_EMAIL

    def test_create_user(self):
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
        UserOrm.create_user(test_user)

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