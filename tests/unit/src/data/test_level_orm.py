import uuid

from sqlalchemy import select, insert

from src.dto.schema import LevelAddDTO
from src.model.level import Level
from src.model.level_enum import LevelEnum
from src.data.level_orm import LevelOrm
from src.db.database import session_factory

from tests.unit.test_data_preparation import (DataPreparation)

class TestLevelOrm:
    """Group of Unit-Tests for class LevelOrm"""

    def test_insert_standard_levels(self):
        """
        Positive test for creating all levels
        """
        # Do tests
        LevelOrm.insert_all_levels()

        # Check results
        with session_factory() as session:
            stmt = select(Level)
            result = session.execute(stmt)
            all_levels = result.scalars().all()

            assert len(all_levels) == 6
            for level in all_levels:
                assert level.lang_level in LevelEnum

    def test_get_all_levels(self):
        """
        Positive test for get_all_levels
        """
        # Prepare data
        LevelOrm.insert_all_levels()

        # Do tests
        levels = LevelOrm.get_all_levels()

        # Check results
        assert len(levels) == 6
        for level in levels:
            assert level.lang_level in LevelEnum

    def test_get_level_id_by_name(self):
        """
        Positive test for get_level_id_by_name
        """

        # Prepare data
        test_uuid = uuid.uuid4()
        with session_factory() as session:
            new_level = LevelAddDTO(lang_level=LevelEnum.a1, id=test_uuid)
            stmt = insert(Level).values(**new_level.dict())
            session.execute(stmt)
            session.commit()

        # Do tests
        level_id = LevelOrm.get_level_id_by_name(LevelEnum.a1)

        # Check results
        assert level_id == test_uuid