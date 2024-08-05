import uuid

from sqlalchemy import insert, select
from src.dto.schema import WordTypeAddDTO
from src.log.logger import log_decorator, CustomLogger
from src.model.word_type import WordTypeEnum, WordType
from src.db.database import session_factory
from src.data.base_orm import BaseOrm

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
    def get_word_type_id(wordType: WordTypeEnum) -> uuid.UUID:
        """
        Get Word Type ID by enum value (WordTypeEnum)
        @param wordType: value
        @return: word type id (UUID)
        """
        with session_factory() as session:
            stmt = select(WordType).filter_by(word_type=wordType)
            result = session.execute(stmt)
            word_type_res = result.scalars().first()
            return word_type_res.id

