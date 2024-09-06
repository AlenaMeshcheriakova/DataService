import uuid
from typing import List
from uuid import UUID

from src.model.action_dwh_enum import ActionDWHEnum
from src.dto.schema import LevelDTO, convert_full_level_dto_to_level_dto, LevelAddDTO
from src.dwh.dwh_service import DwhService
from src.log.logger import log_decorator, logger
from src.model.level_enum import LevelEnum
from src.data.level_orm import LevelOrm

class LevelService:

    @staticmethod
    @log_decorator(my_logger=logger)
    def create_levels() -> None:
        """
        Create all standard levels (from LevelEnum) in DB.
        @return: None
        """
        added_levels = LevelOrm.insert_all_levels()
        for added_level in added_levels:
            DwhService.send('Level',
                            added_level,
                            ActionDWHEnum.CREATED,
                            "New level was added")

    @staticmethod
    @log_decorator(my_logger=logger)
    def create_level(level_name: str) -> None:
        new_level = LevelAddDTO(
            id=uuid.uuid4(),
            lang_level=level_name
        )
        LevelOrm.create_level(new_level)
        return None

    @staticmethod
    @log_decorator(my_logger=logger)
    def get_levels() -> List[LevelDTO]:
        """
        Get all levels from DB
        @return: List of LevelDTO
        """
        res_levels = LevelOrm.get_all_levels()
        return res_levels

    @staticmethod
    @log_decorator(my_logger=logger)
    def get_level_id_by_name(level_enum: str) -> UUID:
        """
        Get Level id by level name(from LevelEnum)
        @param level_enum: str
        @return: level_id (UUID)
        """
        level_id = LevelOrm.get_level_id_by_name(level_enum)
        return level_id

    @staticmethod
    @log_decorator(my_logger=logger)
    def get_level_by_id(level_id: uuid.UUID) -> LevelDTO:
        level = LevelOrm.get_level_by_id(level_id)
        if level is None:
            raise ValueError(f"Level with ID {level_id} not found")
        level_res: LevelDTO = convert_full_level_dto_to_level_dto(level)
        return level_res

    @staticmethod
    @log_decorator(my_logger=logger)
    def update_level(level_id: uuid.UUID, new_level_name: str) -> None:
        level_to_update = LevelOrm.get_level_by_id(level_id)
        if level_to_update is None:
            raise ValueError(f"Level with ID {level_id} wasn't found")
        LevelOrm.update_level(level_id, new_level_name)
        DwhService.send('Level', level_to_update, ActionDWHEnum.UPDATED, f"Level was updated to new lang name {new_level_name}")

    @staticmethod
    @log_decorator(my_logger=logger)
    def delete_level(level_id: uuid.UUID) -> None:
        level_to_delete = LevelOrm.get_level_by_id(level_id)
        if level_to_delete is None:
            raise ValueError(f"Level with ID {level_id} wasn't found")
        LevelOrm.delete_level(level_id)
        DwhService.send('Level', level_to_delete, ActionDWHEnum.DELETED, "Level was deleted")
