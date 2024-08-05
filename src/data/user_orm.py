import uuid
import logging
from typing import Union

from sqlalchemy import select, update

from src.db.database import session_factory
from src.dto.schema import UserCreateFullDTO, UserCreateTelegramDTO
from src.log.logger import log_decorator, CustomLogger
from src.model.userdb import UserDB
from src.data.base_orm import BaseOrm

class UserOrm(BaseOrm):
    """
    UserOrm class for object User which allowed work with User in database
    """

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def find_user_by_name(user_name: str) -> Union[UserCreateFullDTO, None]:
        """
        Get User object by user_name
        @param user_name: user_name
        @return: UserDTO (UserCreateFullDTO)
        """
        with session_factory() as session:
            query = select(UserDB).filter_by(user_name=user_name)
            result = session.execute(query)
            res_all = result.scalars().first()
            if res_all:
                user = UserCreateFullDTO.model_validate(res_all)
                return user
            else:
                return None

    @staticmethod
    def update_training_length(user_name:str, new_training_length: int) -> None:
        """
        Update Training Length for user by user_name
        Should be more than 1
        @return:
        """
        with session_factory() as session:
            stmt = update(UserDB).filter_by(
                user_name=user_name
            ).values(
                training_length=new_training_length
            )
            session.execute(stmt)
            session.commit()

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def find_user_by_id(user_id: uuid.UUID) -> UserCreateFullDTO:
        """
        Get User object by user_id
        @param user_id: user_id
        @return: UserDTO (UserCreateFullDTO)
        """
        with session_factory() as session:
            logging.info('Class UserOrm.find_user_by_id: start session')
            query = select(UserDB).filter_by(id=user_id)
            result = session.execute(query)
            user: UserCreateFullDTO = UserCreateFullDTO.parse_obj(result.scalars().first())
            return user

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def create_user(new_user: UserCreateTelegramDTO) -> None:
        """
        Create user by DTO
        @param new_user: user which will be created
        @return: None
        """
        with session_factory() as session:
            logging.info('Class UserOrm.create_user: start session')
            new_user = UserDB(**new_user.dict())
            session.add(new_user)
            session.commit()




