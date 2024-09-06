from src.log.logger import log_decorator, logger
import uuid
from typing import List, Union
from sqlalchemy import insert, select, update, delete
from src.dto.schema import GroupAddDTO, GroupDTO
from src.model.group import Group
from src.db.database import session_factory
from src.data.base_orm import BaseOrm
from src.model.userdb import UserDB

class GroupOrm(BaseOrm):
    """
    GroupOrm Class for object Group which allowed insert/get Group in database
    """

    @log_decorator(my_logger=logger)
    @staticmethod
    def insert_group(group_name: GroupAddDTO) -> None:
        """
        Insert group name in database
        Note: id will be replaced in the method
        :param group_name: Name of the group
        :return: None
        """
        with session_factory() as session:
            group_name.id = uuid.uuid4()
            stmt = insert(Group).values(**group_name.dict()).returning(Group)
            result = session.execute(stmt)
            session.commit()

            created_group = result.fetchone()
            if created_group:
                return created_group[0]
            else:
                raise RuntimeError("Failed to retrieve created group")
        return None

    @log_decorator(my_logger=logger)
    @staticmethod
    def get_group_by_name(group_name: str) -> Union[GroupDTO, None]:
        """
        Get Group Object by group name from database
        :param group_name: Name of the Group
        :return: GroupID (UUID) or None if group wasn't find
        """
        with (session_factory() as session):
            stmt = select(Group.group_name, Group.id, Group.user_id, Group.updated_at, Group.created_at).filter_by(group_name=group_name)
            result = session.execute(stmt)
            res_first = result.first()
            if res_first:
                group = GroupDTO.model_validate(res_first._asdict())
                return group
            else:
                return None

    @log_decorator(my_logger=logger)
    @staticmethod
    def get_group_by_id(group_id: uuid.UUID) -> Union[GroupDTO, None]:
        """
        Get Group Object by group id from database
        :param group_name: Name of the Group
        :return: GroupID (UUID) or None if group wasn't find
        """
        with (session_factory() as session):
            stmt = select(Group.group_name, Group.id, Group.user_id, Group.updated_at, Group.created_at).filter_by(
                id=group_id)
            result = session.execute(stmt)
            res_first = result.first()
            if res_first:
                group = GroupDTO.model_validate(res_first._asdict())
                return group
            else:
                return None

    @log_decorator(my_logger=logger)
    @staticmethod
    def get_list_groups_name_by_user(user_name: str) -> List[str]:
        """
        Get List of Groups by group name from database
        :param user_name: Name of the User
        :return: List of Group names
        """
        with session_factory() as session:
            stmt = select(Group.group_name).join(
                UserDB, UserDB.id == Group.user_id
            ).where(user_name == user_name)
            result = session.execute(stmt)
            groups = result.scalars().all()
            return groups

    @log_decorator(my_logger=logger)
    @staticmethod
    def update_group(group_id: uuid.UUID, new_group_name: str) -> None:
        """
        Update an existing group's name in the database.
        :param group_id: ID of the group to update
        :param new_group_name: New name for the group
        :return: None
        """
        with (session_factory() as session):
            stmt = update(Group).where(
                Group.id == group_id
            ).values(
                group_name=new_group_name
            ).execution_options(synchronize_session="fetch")

            result = session.execute(stmt)
            if result.rowcount == 0:
                raise ValueError(f"Group with ID {group_id} not found")
            session.commit()

    @log_decorator(my_logger=logger)
    @staticmethod
    def delete_group(group_id: uuid.UUID) -> None:
        """
        Delete a group from the database by its ID.
        :param group_id: ID of the group to delete
        :return: None
        """
        with session_factory() as session:
            stmt = delete(Group).where(Group.id == group_id)
            result = session.execute(stmt)
            if result.rowcount == 0:
                raise ValueError(f"Group with ID {group_id} not found")
            session.commit()