import uuid

from src.model.action_dwh_enum import ActionDWHEnum
from src.dto.schema import UserCreateFullDTO, UserCreateTelegramDTO, RegisterRequest, UserAuthTelegramDTO
from src.data.user_orm import UserOrm
from src.dwh.dwh_service import DwhService
from src.grpc.auth_service.auth_service import AuthService
from src.log.logger import log_decorator, logger

class UserService:
    @staticmethod
    @log_decorator(my_logger=logger)
    def get_user_by_id(user_id: uuid.UUID) -> UserCreateFullDTO:
        """
        Get User object from UserOrm by user_id
        @param user_id: user_id
        @return: UserDTO (UserCreateFullDTO)
        """
        raw_user: UserCreateFullDTO = UserOrm.find_user_by_id(user_id)
        return raw_user

    @staticmethod
    @log_decorator(my_logger=logger)
    def get_user_by_name(user_name: str) -> UserCreateFullDTO:
        """
        Get User object from UserOrm by user_name
        @param user_name: user_name
        @return: UserDTO (UserCreateFullDTO)
        """
        raw_user: UserCreateFullDTO = UserOrm.find_user_by_name(user_name)
        return raw_user

    @staticmethod
    @log_decorator(my_logger=logger)
    def get_user_id_by_name(user_name: str) -> uuid.UUID:
        """
        Get User by name and return its id
        @param user_name:
        @return: user_id (uuid.UUID)
        """
        user_id = UserOrm.find_user_by_name(user_name).id
        return user_id

    @staticmethod
    @log_decorator(my_logger=logger)
    def update_user_training_length(user_name: str, new_training_length: int) -> None:
        """
        Update training length for User by user_name
        @param user_name: user_name
        @return: None
        """
        updated_user = UserOrm.update_training_length(user_name, new_training_length)
        DwhService.send('User', updated_user, ActionDWHEnum.UPDATED, "Training length was updated for user")

    @staticmethod
    @log_decorator(my_logger=logger)
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
    @log_decorator(my_logger=logger)
    def create_user_by_DTO(new_user: UserAuthTelegramDTO) -> None:
        """
        Create user by DTO
        @param new_user: UserCreateTelegramDTO
        @return: None
        """
        # Create AUTH user
        registration_data = RegisterRequest(
            username=new_user.user_name,
            password=new_user.password,
            email=new_user.email,
            telegram_user_id=new_user.telegram_user_id
        )
        res = AuthService.register(registration_data)
        if not res.message:
            raise ValueError(
                f"User with name: {new_user.user_name}, email: {new_user.email} "
                f"and telegram_user_id: {new_user.telegram_user_id} was not created")

        # Create DATA user
        new_data_user = UserCreateTelegramDTO(
            id=new_user.id,
            auth_user_id=new_user.auth_user_id,
            user_name=new_user.user_name,
            training_length=new_user.training_length
        )
        created_user = UserOrm.create_user(new_data_user)
        DwhService.send('User', created_user, ActionDWHEnum.UPDATED, "Create new user")

    @staticmethod
    @log_decorator(my_logger=logger)
    def create_user(name: str, password: str, email: str, telegram_user_id: str, training_length: int = 10) -> None:
        """
        Create user
        @param name: users name
        @param training_length: users training_length (By default 10)
        @return: None
        """
        # Create AUTH user
        registration_data = RegisterRequest(
            username=name,
            password=password,
            email=email,
            telegram_user_id=telegram_user_id
        )
        res = AuthService.register(registration_data)

        # Create DATA user
        new_user = UserCreateTelegramDTO(
            id=uuid.uuid4(),
            user_name=name,
            training_length=training_length
        )
        createdUser = UserOrm.create_user(new_user)
        DwhService.send('User', createdUser, ActionDWHEnum.UPDATED, "Create new user")
