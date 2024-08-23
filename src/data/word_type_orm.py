import uuid

from sqlalchemy import insert, select, update, delete
from src.dto.schema import WordTypeAddDTO, WordTypeDTO
from src.log.logger import log_decorator, CustomLogger
from src.model.word_type import WordType
from src.db.database import session_factory
from src.data.base_orm import BaseOrm
from src.model.word_type_enum import WordTypeEnum


class WordTypeOrm(BaseOrm):

    """
    Class for working with data (WordType) in database
    """
    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def insert_all_word_types() -> None:
        """
        Insert standard word type from WordTypeEnum
        @return: None
        """
        with session_factory() as session:
            for word_type_ in WordTypeEnum:
                wt_dto = WordTypeAddDTO(word_type=word_type_, id=uuid.uuid4())
                stmt = insert(WordType).values(**wt_dto.dict())
                session.execute(stmt)
            session.commit()

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def get_word_type_id(wordType: str) -> uuid.UUID:
        """
        Get Word Type ID by value (wordType)
        @param wordType: str
        @return: word type id (UUID)
        """
        with session_factory() as session:
            stmt = select(WordType).filter_by(word_type=wordType)
            result = session.execute(stmt)
            word_type_res = result.scalars().first()
            if not word_type_res:
                raise ValueError(f"Word Type with wordType {wordType} not found")
            else:
                return word_type_res.id

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def insert_word_type(word_type_dto: WordTypeAddDTO) -> None:
        with session_factory() as session:
            stmt = insert(WordType).values(**word_type_dto.dict())
            session.execute(stmt)
            session.commit()

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def update_word_type(word_type_id: uuid.UUID, new_word_type: str) -> None:
        with session_factory() as session:
            stmt = update(WordType).where(WordType.id == word_type_id).values(word_type=new_word_type)
            session.execute(stmt)
            session.commit()

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def delete_word_type(word_type_id: uuid.UUID) -> bool:
        with session_factory() as session:
            stmt = delete(WordType).where(WordType.id == word_type_id)
            result = session.execute(stmt)
            session.commit()
            return result.rowcount > 0


