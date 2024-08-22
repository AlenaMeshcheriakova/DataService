import uuid
from typing import List, Dict, Union
import logging

from sqlalchemy import insert, select, update, delete
from src.data.orm_const import QUERY_AMOUNT_LIMIT
from src.log.logger import log_decorator, CustomLogger
from src.model.level import Level, LevelEnum
from src.db.database import session_factory
from src.dto.schema import LevelAddDTO, LevelDTO, LevelFullDTO
from src.data.base_orm import BaseOrm


class LevelOrm(BaseOrm):
    """
    LevelOrm class for object Level which allowed work with Level in database
    """
    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def insert_all_levels() -> List[Dict]:
        """
        Create all necessary level in DB.
        Level information get from LevelEnum
        @return: None
        """
        created_levels = list()
        with session_factory() as session:
            for level in LevelEnum:
                new_level = LevelAddDTO(lang_level=level, id=uuid.uuid4())
                stmt = insert(Level).values(**new_level.dict()).returning(Level)
                result = session.execute(stmt)
                created_level = result.fetchone()
                if created_level:
                    created_levels.append(created_level[0].as_dict())
            session.commit()
        return created_levels

    @log_decorator(my_logger=CustomLogger())
    def create_level(level: LevelAddDTO) -> None:
        """
        Insert a single level into the DB
        @param level: LevelAddDTO
        @return: None
        """
        with session_factory() as session:
            stmt = insert(Level).values(**level.dict())
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
    def get_level_id_by_name(enum_example: str) -> uuid.UUID:
        """
        Get Level id by level name
        @param enum_example: value in str
        @return: level id (UUID)
        """
        with session_factory() as session:
            query = select(Level).filter_by(lang_level=enum_example)
            result = session.execute(query)
            level = result.scalars().first()
            return level.id

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def get_level_by_id(level_id: uuid.UUID) -> Union[LevelFullDTO, None]:
        """
        Get a level by ID.
        @param level_id: UUID of the level.
        @return: LevelDTO or None if not found.
        """
        with session_factory() as session:
            query = select(Level).filter_by(id=level_id)
            result = session.execute(query)
            level = result.scalars().first()
            if level:
                return LevelFullDTO(
                    id=level.id,
                    lang_level=level.lang_level,
                    created_at=level.created_at,
                    updated_at=level.updated_at
                )
            return None

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def update_level(level_id: uuid.UUID, new_level_name: str) -> None:
        """
        Update a level in the database.
        @param level_id: UUID of the level to update.
        @param updated_data: Dictionary with updated data.
        @return: None.
        """
        with session_factory() as session:
            stmt = update(Level).where(Level.id == level_id).values(lang_level=new_level_name)
            session.execute(stmt)
            session.commit()

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def delete_level(level_id: uuid.UUID) -> None:
        """
        Delete a level from the database by ID.
        @param level_id: UUID of the level to delete.
        @return: None.
        """
        with session_factory() as session:
            stmt = delete(Level).where(Level.id == level_id)
            session.execute(stmt)
            session.commit()