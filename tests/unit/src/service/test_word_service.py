import uuid

from level_enum import LevelEnum
from src.data.word_orm import WordOrm
from src.db.database import session_factory
from sqlalchemy import select

from src.dto.schema import WordDTO, WordAddDTO
from src.model.word import Word
from src.service.word_service import WordService
from tests.unit.test_data_preparation import (DataPreparation, create_test_user, create_list_test_words,
                                              create_mini_list_test_words, create_test_level, create_test_group,
                                              create_test_word_type, create_test_word)

class TestWordService:
    """Group of Unit-Tests for class WordService"""

    def test_get_words_by_user(self, create_test_user, create_test_level, create_test_group,
                                    create_test_word_type, create_list_test_words):
        """
        Positive Test for selecting standard training set
        """
        # Do tests
        word_set = WordService.get_words_by_user(DataPreparation.TEST_USER_ID, 10, DataPreparation.TEST_WORD_TYPE)

        # Check results
        assert len(word_set) == 10
        for word in word_set:
            assert word.user_id == DataPreparation.TEST_USER_ID
            assert word.word_type_id == DataPreparation.TEST_WORD_TYPE_ID
            assert word.group_id == DataPreparation.TEST_GROUP_ID
            assert word.amount_back_to_learning == 0
            assert word.amount_already_know == 0
            assert word.german_word in [test_word.get('german_word') for test_word in DataPreparation.TEST_WORD_DICT]
            assert word.russian_word in [test_word.get('russian_word') for test_word in DataPreparation.TEST_WORD_DICT]
            assert word.english_word in [test_word.get('english_word') for test_word in DataPreparation.TEST_WORD_DICT]
        german_word_list = [word.german_word for word in word_set]
        german_word_set = set(german_word_list)
        assert len(german_word_set) == len(german_word_list)

    def test_get_words_by_user_mini_set(self, create_test_user, create_test_level, create_test_group,
                                    create_test_word_type, create_mini_list_test_words):
        """
        Test for selecting training set when user have word less than training amount
        """
        # Do tests
        word_set = WordService.get_words_by_user(DataPreparation.TEST_USER_ID, 10, DataPreparation.TEST_WORD_TYPE)

        # Check results
        assert len(word_set) == len(DataPreparation.TEST_WORD_DICT_MINI)
        for word in word_set:
            assert word.user_id == DataPreparation.TEST_USER_ID
            assert word.word_type_id == DataPreparation.TEST_WORD_TYPE_ID
            assert word.group_id == DataPreparation.TEST_GROUP_ID
            assert word.amount_back_to_learning == 0
            assert word.amount_already_know == 0
            assert word.german_word in [test_word.get('german_word') for test_word in DataPreparation.TEST_WORD_DICT_MINI]
            assert word.russian_word in [test_word.get('russian_word') for test_word in DataPreparation.TEST_WORD_DICT_MINI]
            assert word.english_word in [test_word.get('english_word') for test_word in DataPreparation.TEST_WORD_DICT_MINI]
        german_word_list = [word.german_word for word in word_set]
        german_word_set = set(german_word_list)
        assert len(german_word_set) == len(german_word_list)

    def test_get_words_by_user_limited_set_amount(self, create_test_user, create_test_level, create_test_group,
                                    create_test_word_type,create_list_test_words):
        """
        Test for selecting standard training set, but set a set length limit to 3
        """
        # Do tests
        word_set = WordService.get_words_by_user(DataPreparation.TEST_USER_ID, 3, DataPreparation.TEST_WORD_TYPE)

        # Check results
        assert len(word_set) == 3
        for word in word_set:
            assert word.user_id == DataPreparation.TEST_USER_ID
            assert word.word_type_id == DataPreparation.TEST_WORD_TYPE_ID
            assert word.group_id == DataPreparation.TEST_GROUP_ID
            assert word.amount_back_to_learning == 0
            assert word.amount_already_know == 0
            assert word.german_word in [test_word.get('german_word') for test_word in DataPreparation.TEST_WORD_DICT]
            assert word.russian_word in [test_word.get('russian_word') for test_word in DataPreparation.TEST_WORD_DICT]
            assert word.english_word in [test_word.get('english_word') for test_word in DataPreparation.TEST_WORD_DICT]

    def test_add_word(self, create_test_user, create_test_level, create_test_group, create_test_word_type):
        """
        Positive Test for method add_word
        """

        # Prepare data
        word = DataPreparation.TEST_WORD
        tested_word = WordAddDTO(
            user_id= DataPreparation.TEST_USER_ID,
            german_word= word.get('german_word'),
            english_word= word.get('english_word'),
            russian_word= word.get('russian_word'),
            amount_already_know= 0,
            amount_back_to_learning= 0,
            lang_level_id= DataPreparation.TEST_LEVEL_ID,
            word_type_id= DataPreparation.TEST_WORD_TYPE_ID,
            group_id= DataPreparation.TEST_GROUP_ID
        )

        # Do tests
        WordService.add_new_word_from_dto(tested_word)

        # Check results
        with session_factory() as session:
            query = select(Word)
            result = session.execute(query)
            res_word = result.scalars().all()
            tested_word = res_word[0]

            assert len(res_word) == 1
            assert tested_word.user_id == DataPreparation.TEST_USER_ID
            assert tested_word.word_type_id == DataPreparation.TEST_WORD_TYPE_ID
            assert tested_word.group_id == DataPreparation.TEST_GROUP_ID
            assert tested_word.amount_back_to_learning == 0
            assert tested_word.amount_already_know == 0
            assert tested_word.german_word == word.get('german_word')
            assert tested_word.russian_word == word.get('russian_word')
            assert tested_word.english_word == word.get('english_word')

    def test_add_new_word(self, create_test_user, create_test_level, create_test_group, create_test_word_type):
        """
        Positive Test for method add_word
        """
        # Prepare data
        word = DataPreparation.TEST_WORD

        # Do tests
        WordService.add_new_word(DataPreparation.TEST_USER_NAME, word.get('german_word'), word.get('english_word'),
                                 word.get('russian_word'), 0, 0,
                                 group_word_name=DataPreparation.TEST_GROUP_NAME, level=LevelEnum.a1,
                                 word_type=DataPreparation.TEST_WORD_TYPE)

        # Check results
        with session_factory() as session:
            query = select(Word)
            result = session.execute(query)
            res_word = result.scalars().all()
            tested_word = res_word[0]

            assert len(res_word) == 1
            assert tested_word.user_id == DataPreparation.TEST_USER_ID
            assert tested_word.word_type_id == DataPreparation.TEST_WORD_TYPE_ID
            assert tested_word.group_id == DataPreparation.TEST_GROUP_ID
            assert tested_word.amount_back_to_learning == 0
            assert tested_word.amount_already_know == 0
            assert tested_word.german_word == word.get('german_word')
            assert tested_word.russian_word == word.get('russian_word')
            assert tested_word.english_word == word.get('english_word')