import uuid
from typing import List
import logging

from sqlalchemy import insert, select
from src.data.orm_const import QUERY_AMOUNT_LIMIT
from src.log.logger import log_decorator, CustomLogger
from src.model.level import Level, LevelEnum
from src.db.database import session_factory
from src.dto.schema import LevelAddDTO, LevelDTO
from src.data.base_orm import BaseOrm


class LevelOrm(BaseOrm):
    """
    LevelOrm class for object Level which allowed work with Level in database
    """
    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def insert_all_levels() -> None:
        """
        Create all necessary level in DB.
        Level information get from LevelEnum
        @return: None
        """
        with session_factory() as session:
            for level in LevelEnum:
                new_level = LevelAddDTO(lang_level=level, id=uuid.uuid4())
                stmt = insert(Level).values(**new_level.dict())
                session.execute(stmt)
            session.commit()

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def get_all_levels() -> List[LevelDTO]:
        """
        Get List of existed levels
        @return: list of Levels (LevelDTO)
        """
        with session_factory() as session:
            query = select(Level).limit(QUERY_AMOUNT_LIMIT)
            result = session.execute(query)
            result_all = result.scalars().all()
            levels = [
                LevelDTO(
                    lang_level=level.lang_level,
                    created_at=level.created_at,
                    updated_at=level.updated_at
                )
                for level in result_all
            ]
            return levels

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def get_level_id_by_name(enum_example: LevelEnum) -> uuid.UUID:
        """
        Get Level id by level name(from LevelEnum)
        @param enum_example: value in LevelEnum
        @return: level id (UUID)
        """
        with session_factory() as session:
            query = select(Level).filter_by(lang_level=enum_example)
            result = session.execute(query)
            level = result.scalars().first()
            return level.id

