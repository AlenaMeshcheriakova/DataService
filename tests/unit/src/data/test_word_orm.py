import uuid

from src.data.word_orm import WordOrm
from src.db.database import session_factory
from sqlalchemy import select

from src.dto.schema import WordDTO
from src.model.word import Word
from tests.unit.test_data_preparation import (DataPreparation, create_test_user, create_list_test_words,
                                              create_mini_list_test_words, create_test_level, create_test_group,
                                              create_test_word_type, create_test_word)

class TestWordOrm:
    """Group of Unit-Tests for class WordOrm"""

    def test_find_words_by_user_id_without_words(self, create_test_user):
        """
        Test for selecting standard training set without creating words before
        """
        # Do tests
        word_set = WordOrm.find_words_by_user_id(DataPreparation.TEST_USER_ID)

        assert len(word_set) == 0

    def test_find_words_by_user_id(self, create_test_user, create_test_level, create_test_group,
                                    create_test_word_type,create_list_test_words):
        """
        Positive Test for selecting standard training set
        """
        # Do tests
        word_set = WordOrm.find_words_by_user_id(DataPreparation.TEST_USER_ID, 10, DataPreparation.TEST_WORD_TYPE)

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

    def test_find_words_by_user_id_mini_set(self, create_test_user, create_test_level, create_test_group,
                                    create_test_word_type, create_mini_list_test_words):
        """
        Test for selecting training set when user have word less than training amount
        """
        # Do tests
        word_set = WordOrm.find_words_by_user_id(DataPreparation.TEST_USER_ID, 10, DataPreparation.TEST_WORD_TYPE)

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

    def test_find_words_by_user_id_limited_set_amount(self, create_test_user, create_test_level, create_test_group,
                                    create_test_word_type,create_list_test_words):
        """
        Test for selecting standard training set, but set a set length limit to 3
        """
        # Do tests
        word_set = WordOrm.find_words_by_user_id(DataPreparation.TEST_USER_ID, 3, DataPreparation.TEST_WORD_TYPE)

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

    def test_find_word_by_id(self, create_test_user, create_test_level, create_test_group,
                             create_test_word_type, create_test_word):
        """
        Positive test for find_word_by_id
        """
        # Do tests
        try:
            WordOrm.find_word_by_id(None)
        except ValueError as ex:
            # Check results
            assert ex.args[0] == "Word ID is None: None, expected UUID"

    def test_add_word(self, create_test_user, create_test_level, create_test_group, create_test_word_type):
        """
        Positive Test for method add_word
        """

        # Prepare data
        word = DataPreparation.TEST_WORD
        tested_word = WordDTO(
            id = uuid.uuid4(),
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
        WordOrm.add_word(tested_word)

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

    def test_add_word_with_none(self, create_test_user, create_test_level, create_test_group, create_test_word_type):
        """
        Test method add_word with None parameter
        """

        # Do tests
        try:
            WordOrm.add_word(None)
        except ValueError as ex:
            # Check results
            assert ex.args[0] == "Word is None: None, expected WordDTO"

    def test_update_counter_for_word(self, create_test_user, create_test_level, create_test_group,
                                     create_test_word_type, create_test_word):
        """
        Positive method update_counter_for_word
        """
        # Prepare data
        test_amount_back_to_learning = 1
        test_amount_already_know = 3

        # Do tests
        WordOrm.update_counter_for_word(DataPreparation.TEST_WORD.get('german_word'), DataPreparation.TEST_USER_ID,
                                        test_amount_already_know, test_amount_back_to_learning)

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
            assert tested_word.amount_back_to_learning == test_amount_back_to_learning
            assert tested_word.amount_already_know == test_amount_already_know
            assert tested_word.german_word == DataPreparation.TEST_WORD.get('german_word')
            assert tested_word.russian_word == DataPreparation.TEST_WORD.get('russian_word')
            assert tested_word.english_word == DataPreparation.TEST_WORD.get('english_word')


    def check_counter_for_word(self, create_test_user, create_test_level, create_test_group,
                                     create_test_word_type, create_test_word,
                                test_amount_back_to_learning: int = 1, test_amount_already_know: int = 3):
        """
        Used in the next tests with different paramenets
        @param create_test_user: create test user with data from DataPreparation
        @param create_test_level: create test Level with data from DataPreparation
        @param create_test_group: create test group with data from DataPreparation
        @param create_test_word_type: create word type  with data from DataPreparation
        @param create_test_word: create one test word with data from DataPreparation
        @param test_amount_back_to_learning: configurable parameter, have to be set in test
        @param test_amount_already_know: configurable parameter, have to be set in test
        """
        # Do tests
        WordOrm.update_counter_for_word(DataPreparation.TEST_WORD.get('german_word'), DataPreparation.TEST_USER_ID,
                                        test_amount_already_know, test_amount_back_to_learning)

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
            assert tested_word.amount_back_to_learning == test_amount_back_to_learning
            assert tested_word.amount_already_know == test_amount_already_know
            assert tested_word.german_word == DataPreparation.TEST_WORD.get('german_word')
            assert tested_word.russian_word == DataPreparation.TEST_WORD.get('russian_word')
            assert tested_word.english_word == DataPreparation.TEST_WORD.get('english_word')

    def test_word_counter_variant_with_0_back_to_learning(self, create_test_user, create_test_level, create_test_group,
                                     create_test_word_type, create_test_word):
        self.check_counter_for_word(create_test_user, create_test_level, create_test_group,
                                     create_test_word_type, create_test_word,
                                     test_amount_back_to_learning = 0, test_amount_already_know = 3)

    def test_word_counter_variant_with_0_already_know(self, create_test_user, create_test_level, create_test_group,
                                     create_test_word_type, create_test_word):
        self.check_counter_for_word(create_test_user, create_test_level, create_test_group,
                                     create_test_word_type, create_test_word,
                                     test_amount_back_to_learning = 3, test_amount_already_know = 0)

    def test_word_counter_variant_with_huge_back_to_learning(self, create_test_user, create_test_level, create_test_group,
                                     create_test_word_type, create_test_word):
        self.check_counter_for_word(create_test_user, create_test_level, create_test_group,
                                     create_test_word_type, create_test_word,
                                     test_amount_back_to_learning = 1, test_amount_already_know = 111)

    def test_word_counter_variant_with_huge_already_know(self, create_test_user, create_test_level, create_test_group,
                                     create_test_word_type, create_test_word):
        self.check_counter_for_word(create_test_user, create_test_level, create_test_group,
                                     create_test_word_type, create_test_word,
                                     test_amount_back_to_learning = 999, test_amount_already_know = 1)

    def test_update_counter_for_word_negative_amount(self, create_test_user, create_test_level, create_test_group,
                                     create_test_word_type, create_test_word):
        """
        Positive method update_counter_for_word
        """
        # Prepare data
        test_amount_back_to_learning = -1
        test_amount_already_know = 3

        # Do tests
        try:
            WordOrm.update_counter_for_word(DataPreparation.TEST_WORD.get('german_word'), DataPreparation.TEST_USER_ID,
                                            test_amount_already_know, test_amount_back_to_learning)

        except ValueError as ex:
            # Check results
            assert ex.args[0] == f"Updated word parameters have to be > 0: {test_amount_already_know} or {test_amount_back_to_learning}"
