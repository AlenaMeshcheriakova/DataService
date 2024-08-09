import uuid

from action_dwh_enum import ActionDWHEnum
from src.dto.schema import UserCreateFullDTO, UserCreateTelegramDTO
from src.data.user_orm import UserOrm
from src.dwh.dwh_service import DwhService
from src.log.logger import log_decorator, CustomLogger

class UserService:
    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def get_user_by_id(user_id: uuid.UUID) -> UserCreateFullDTO:
        """
        Get User object from UserOrm by user_id
        @param user_id: user_id
        @return: UserDTO (UserCreateFullDTO)
        """
        raw_user: UserCreateFullDTO = UserOrm.find_user_by_id(user_id)
        return raw_user

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def get_user_by_name(user_name: str) -> UserCreateFullDTO:
        """
        Get User object from UserOrm by user_name
        @param user_name: user_name
        @return: UserDTO (UserCreateFullDTO)
        """
        raw_user: UserCreateFullDTO = UserOrm.find_user_by_name(user_name)
        return raw_user

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def get_user_id_by_name(user_name: str) -> uuid.UUID:
        """
        Get User by name and return its id
        @param user_name:
        @return: user_id (uuid.UUID)
        """
        user_id = UserOrm.find_user_by_name(user_name).id
        return user_id

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def update_user_training_length(user_name: str, new_training_length: int) -> None:
        """
        Update training length for User by user_name
        @param user_name: user_name
        @return: None
        """
        updated_user = UserOrm.update_training_length(user_name, new_training_length)
        DwhService.send('User', updated_user, ActionDWHEnum.UPDATED, "Training length was updated for user")

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def is_user_created(user_name: str) -> bool:
        """
        Check is User with user_name was created.
        @param user_name: user_name
        @return: Return True if exist and False if is not
        """
        raw_user = UserOrm.find_user_by_name(user_name)
        if raw_user is None:
            return False
        else:
            return True

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def create_user_by_DTO(new_user: UserCreateTelegramDTO) -> None:
        """
        Create user by DTO
        @param new_user: UserCreateTelegramDTO
        @return: None
        """
        createdUser = UserOrm.create_user(new_user)
        DwhService.send('User', createdUser, ActionDWHEnum.UPDATED, "Create new user")

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def create_user(name: str, email: str, password: str, telegram_id: str, training_length: int = 10) -> None:
        """
        Create user
        @param name: users name
        @param email: users email
        @param password: users password
        @param telegram_id: users telegram_id
        @param training_length: users training_length (By default 10)
        @return: None
        """
        new_user = UserCreateTelegramDTO(
            id=uuid.uuid4(),
            user_name=name,
            training_length=training_length,
            telegram_user_id=str(telegram_id),
            hashed_password=str(password),
            email=email
        )
        createdUser = UserOrm.create_user(new_user)
        DwhService.send('User', createdUser, ActionDWHEnum.UPDATED, "Create new user")
