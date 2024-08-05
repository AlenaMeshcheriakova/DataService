from typing import List
from uuid import UUID

from src.dto.schema import LevelDTO
from src.log.logger import log_decorator, CustomLogger
from src.model.level_enum import LevelEnum
from src.data.level_orm import LevelOrm

class LevelService:

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def create_levels() -> None:
        """
        Create all standard levels (from LevelEnum) in DB.
        @return: None
        """
        LevelOrm.insert_all_levels()

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def get_levels() -> List[LevelDTO]:
        """
        Get all levels from DB
        @return: List of LevelDTO
        """
        res_levels = LevelOrm.get_all_levels()
        return res_levels

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def get_level_id_by_name(level_enum: LevelEnum) -> UUID:
        """
        Get Level id by level name(from LevelEnum)
        @param level_enum: value in LevelEnum
        @return: level_id (UUID)
        """
        level_id = LevelOrm.get_level_id_by_name(level_enum)
        return level_id

