import uuid
from typing import List

from src.model.action_dwh_enum import ActionDWHEnum
from src.dwh.dwh_service import DwhService
from src.model.level_enum import LevelEnum
from src.dto.schema import WordGetDTO, WordAddDTO, WordDTO, convert_word_dto_to_word_get_dto
from src.data.word_orm import WordOrm
from src.log.logger import log_decorator, CustomLogger
from src.service.group_word_service import GroupWordService
from src.service.level_service import LevelService
from src.service.user_service import UserService
from src.service.word_type_service import WordTypeService
from src.model.word_type_enum import WordTypeEnum


class WordService:

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def get_words_by_user(user_id: uuid.UUID, training_length: int = 10,
                              word_type: str = WordTypeEnum.custom.value) -> List[WordGetDTO]:
        """
        Find set of words with training length for next training for user with user_id and limited by training_length
        @param user_id: user_id
        @param training_length: training length (10 by default)
        @return:
        """
        training_set: List[WordDTO] = WordOrm.find_words_by_user_id(user_id, training_length, word_type)
        training_set: List[WordGetDTO] = convert_word_dto_to_word_get_dto(training_set)
        return training_set

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def add_new_word_from_dto(word: WordAddDTO) -> None:
        """
        Add new word for learning from dto to user (linked by user_id)
        @param new_word: Word data
        @return: None
        """
        word_data = word.dict()
        word_data.update({
            "id": uuid.uuid4()
        })
        new_word = WordDTO(**word_data)
        added_word = WordOrm.add_word(new_word)
        DwhService.send('Word', added_word, ActionDWHEnum.CREATED, "New word from DTO was added")


    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def add_new_word(user_name: str, german_word: str, english_word: str, russian_word: str,
                     amount_already_know: int = 0, amount_back_to_learning: int = 0,
                     group_word_name: str = "CUSTOM_GROUP", level: str = LevelEnum.a1.value,
                     word_type: str = WordTypeEnum.custom) -> None:
        """
        Add new Word for user by parameters
        @param user_name: user_name (Find User Id first)
        @param german_word: german_word
        @param english_word: english_word
        @param russian_word: russian_word
        @param amount_already_know: 0 By default
        @param amount_back_to_learning: 0 By default
        @param group_word_name: group_word_name (Find Group ID first)
        @param level: word level (Find level ID first)
        @param word_type: word_type (Find word_type ID first)
        @return: None
        """
        # getLevelByDefault by now - level_id
        level_id = LevelService.get_level_id_by_name(level)
        # getUserId by user_name
        user_id = UserService.get_user_id_by_name(user_name)
        # word_type_id by group_name
        word_type_id = WordTypeService.get_word_type_id(word_type)
        # get group_id
        group_word_id = GroupWordService.get_group_id_by_group_name(group_word_name)
        wordAddDTO = WordDTO.model_validate(
            {
                'id': uuid.uuid4(),
                'user_id': user_id,
                'german_word': german_word,
                'english_word': english_word,
                'russian_word': russian_word,
                'amount_already_know': amount_already_know,
                'amount_back_to_learning': amount_back_to_learning,
                'lang_level_id': level_id,
                'word_type_id': word_type_id,
                'group_id': group_word_id
            }
        )
        added_word = WordOrm.add_word(wordAddDTO)
        DwhService.send('Word', added_word, ActionDWHEnum.CREATED, "New word was added")

