import uuid

from sqlalchemy import select, insert
from src.data.word_type_orm import WordTypeOrm
from src.db.database import session_factory
from src.dto.schema import WordTypeAddDTO
from src.model.word_type import WordType
from src.model.word_type_enum import WordTypeEnum

from tests.unit.test_data_preparation import (DataPreparation)

class TestWordTypeOrm:
    """Group of Unit-Tests for class WordTypeOrm"""


    def test_insert_all_custom_word_types(self):
        """
        Positive test for creating all word types
        """
        # Do tests
        WordTypeOrm.insert_all_word_types()

        # Check results
        with session_factory() as session:
            stmt = select(WordType)
            result = session.execute(stmt)
            all_word_types = result.scalars().all()

            assert len(all_word_types) == 3
            for type in all_word_types:
                assert type.word_type in WordTypeEnum

    def test_get_word_type_id(self):
        """
        Positive test for get word type id by name
        """
        # Prepare data
        tested_word_type = WordTypeEnum.test
        test_uuid = uuid.uuid4()
        with session_factory() as session:
            new_word_type = WordTypeAddDTO(word_type=tested_word_type, id=test_uuid)
            stmt = insert(WordType).values(**new_word_type.dict())
            session.execute(stmt)
            session.commit()

        # Do tests
        test_word_type_id = WordTypeOrm.get_word_type_id(tested_word_type)

        assert test_word_type_id == test_uuid