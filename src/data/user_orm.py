import uuid
import logging
from typing import Union

from sqlalchemy import select, update

from src.db.database import session_factory
from src.dto.schema import UserCreateFullDTO, UserCreateTelegramDTO
from src.log.logger import log_decorator, logger
from src.model.userdb import UserDB
from src.data.base_orm import BaseOrm

class UserOrm(BaseOrm):
    """
    UserOrm class for object User which allowed work with User in database
    """

    @staticmethod
    @log_decorator(my_logger=logger)
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
                user = UserCreateFullDTO(
                    id=res_all.id,
                    user_name=res_all.user_name,
                    training_length=res_all.training_length,
                    auth_user_id=res_all.auth_user_id,
                    created_at=res_all.created_at,
                    updated_at=res_all.updated_at
                )
                return user
            else:
                return None

    @staticmethod
    def update_training_length(user_name:str, new_training_length: int) -> UserDB:
        """
        Update Training Length for user by user_name
        Should be more than 1
        @return: UserDB - user which was changed
        """
        with session_factory() as session:
            stmt = update(UserDB).filter_by(
                user_name=user_name
            ).values(
                training_length=new_training_length
            ).returning(UserDB)
            result = session.execute(stmt)
            session.commit()

            updated_user = result.fetchone()
            if updated_user:
                updated_user[0]
            else:
                raise RuntimeError("Failed to retrieve created user")

        return None

    @staticmethod
    @log_decorator(my_logger=logger)
    def find_user_by_id(user_id: uuid.UUID) -> Union[UserCreateFullDTO, None]:
        """
        Get User object by user_id
        @param user_id: user_id
        @return: UserDTO (UserCreateFullDTO)
        """
        with session_factory() as session:
            logging.info('Class UserOrm.find_user_by_id: start session')
            query = select(UserDB).filter_by(id=user_id)
            result = session.execute(query)
            res_all = result.scalars().first()
            if res_all:
                user = UserCreateFullDTO(
                    id=res_all.id,
                    user_name=res_all.user_name,
                    training_length=res_all.training_length,
                    auth_user_id=res_all.auth_user_id,
                    created_at=res_all.created_at,
                    updated_at=res_all.updated_at
                )
                return user
            else:
                return None

    @staticmethod
    @log_decorator(my_logger=logger)
    def create_user(new_user: UserCreateTelegramDTO) -> UserDB:
        """
        Create user by DTO
        @param new_user: user which will be created
        @return: UserDB - user which was created
        """
        with session_factory() as session:
            logging.info('Class UserOrm.create_user: start session')
            new_user = UserDB(**new_user.dict())
            session.add(new_user)
            session.commit()

            fetched_user = session.query(UserDB).filter_by(id=new_user.id).one_or_none()
            return fetched_user





