from uuid import UUID

from src.data.word_type_orm import WordTypeOrm
from src.log.logger import log_decorator, CustomLogger
from src.model.word_type_enum import WordTypeEnum

class WordTypeService:

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def create_all_word_types() -> None:
        """
        Insert standard word types from WordTypeEnum
        @return:
        """
        WordTypeOrm.insert_all_word_types()

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def get_word_type_id(wordType: WordTypeEnum) -> UUID:
        """
        Get Word Type ID by value (should be enum - WordTypeEnum)
        @param wordType: value
        @return: UUID
        """
        word_type_id = WordTypeOrm.get_word_type_id(wordType)
        return word_type_id


