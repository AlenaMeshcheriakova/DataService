import uuid
from uuid import UUID

from src.data.word_type_orm import WordTypeOrm
from src.dto.schema import WordTypeAddDTO
from src.log.logger import log_decorator, logger

class WordTypeService:

    @staticmethod
    @log_decorator(my_logger=logger)
    def create_all_word_types() -> None:
        """
        Insert standard word types from WordTypeEnum
        @return:
        """
        WordTypeOrm.insert_all_word_types()

    @staticmethod
    @log_decorator(my_logger=logger)
    def get_word_type_id(wordType: str) -> UUID:
        """
        Get Word Type ID by value (should be str - WordTypeEnum)
        @param wordType: value
        @return: UUID
        """
        word_type_id = WordTypeOrm.get_word_type_id(wordType)
        return word_type_id

    @staticmethod
    @log_decorator(my_logger=logger)
    def create_word_type(word_type: str) -> uuid.UUID:
        new_word_type = WordTypeAddDTO(id=uuid.uuid4(), word_type=word_type)
        WordTypeOrm.insert_word_type(new_word_type)
        return new_word_type.id

    @staticmethod
    @log_decorator(my_logger=logger)
    def update_word_type(word_type_id: uuid.UUID, new_word_type: str) -> None:
        WordTypeOrm.update_word_type(word_type_id, new_word_type)
        return None

    @staticmethod
    @log_decorator(my_logger=logger)
    def delete_word_type(word_type_id: uuid.UUID):
        WordTypeOrm.delete_word_type(word_type_id)
        return None
