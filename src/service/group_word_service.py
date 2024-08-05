from typing import List
from uuid import UUID

from src.dto.schema import GroupAddDTO
from src.data.group_orm import GroupOrm
from src.log.logger import log_decorator, CustomLogger


class GroupWordService:
    """
    Service Layer which allowed to work with request to Group Data Layer
    """

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def get_groups_name_by_user_name(user_name: str) -> List[str]:
        """
        By user_name get list of users groups name
        @param user_name: user_name
        @return: List of groups name (not a group object)
        """
        res_group_list = GroupOrm.get_list_groups_name_by_user(user_name)
        return res_group_list

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def create_group(new_group: GroupAddDTO) -> None:
        """
        Add new group to the DB
        @param new_group: new group
        @return: None
        """
        GroupOrm.insert_group(new_group)

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def get_group_id_by_group_name(group_name: str) -> UUID:
        """
        Get Group Object by group_name.
        @param group_name: group_name
        @return: group_id
        """
        res_group = GroupOrm.get_group_by_name(group_name)
        if res_group is None:
            raise ValueError(f"Group by name {group_name} wasn't find")
        res_group_id = res_group.id
        return res_group_id

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def is_group_created(group_name: str) -> bool:
        """
        Check that group with group_name exist
        @param group_name: group_name
        @return: group_id
        """
        res_group = GroupOrm.get_group_by_name(group_name)
        if res_group is None:
            return False
        else:
            return True