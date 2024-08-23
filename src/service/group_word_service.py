from typing import List
from uuid import UUID

from src.model.action_dwh_enum import ActionDWHEnum
from src.dto.schema import GroupAddDTO
from src.data.group_orm import GroupOrm
from src.dwh.dwh_service import DwhService
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
        added_group = GroupOrm.insert_group(new_group)
        DwhService.send('Group', added_group, ActionDWHEnum.CREATED, "New group from DTO was added")

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

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def update_group(group_id: UUID, new_group_name: str) -> None:
        """
        Update an existing group's name
        @param group_id: ID of the group to update
        @param new_group_name: New name for the group
        @return: None
        """
        group_to_update = GroupOrm.get_group_by_id(group_id)
        if group_to_update is None:
            raise ValueError(f"Group with ID {group_id} wasn't found")

        group_to_update.group_name = new_group_name
        GroupOrm.update_group(group_id, new_group_name)

        DwhService.send('Group', group_to_update, ActionDWHEnum.UPDATED, f"Group with ID {group_id} was updated")

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def delete_group(group_id: UUID) -> None:
        """
        Delete a group from the DB
        @param group_id: ID of the group to delete
        @return: None
        """
        group_to_delete = GroupOrm.get_group_by_id(group_id)
        if group_to_delete is None:
            raise ValueError(f"Group with ID {group_id} wasn't found")
        GroupOrm.delete_group(group_id)
        DwhService.send('Group', group_to_delete, ActionDWHEnum.DELETED, f"Group with ID {group_id} was deleted")

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def update_group(group_id: UUID, new_group_name: str) -> None:
        """
        Update an existing group's name
        @param group_id: ID of the group to update
        @param new_group_name: New name for the group
        @return: None
        """
        group_to_update = GroupOrm.get_group_by_id(group_id)
        if group_to_update is None:
            raise ValueError(f"Group with ID {group_id} wasn't found")

        group_to_update.group_name = new_group_name
        GroupOrm.update_group(group_id, new_group_name)

        DwhService.send('Group', group_to_update, ActionDWHEnum.UPDATED, f"Group with ID {group_id} was updated")

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def delete_group(group_id: UUID) -> None:
        """
        Delete a group from the DB
        @param group_id: ID of the group to delete
        @return: None
        """
        group_to_delete = GroupOrm.get_group_by_id(group_id)
        if group_to_delete is None:
            raise ValueError(f"Group with ID {group_id} wasn't found")
        GroupOrm.delete_group(group_id)
        DwhService.send('Group', group_to_delete, ActionDWHEnum.DELETED, f"Group with ID {group_id} was deleted")