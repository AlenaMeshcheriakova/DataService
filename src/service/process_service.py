import uuid

from cfg.const import Constant
from src.data.standard_word_user_orm import StandardWordUserOrm
from src.data.user_orm import UserOrm
from src.data.word_orm import WordOrm
from user_action_enum import UserActionEnum
from src.redis.redis_client import RedisImplementation
from src.dto.learning_set import LearningSet
from src.dto.schema import StandardWordDTO
from src.model.word_type_enum import WordTypeEnum


class ProcessService:

    # --------------------WORKING WITH REDIS--------------------
    @staticmethod
    def get_learning_set(user_name: str, word_type: WordTypeEnum) -> LearningSet:
        """
        Get Learning set from Redis
        @param user_name: by user_name
        @param word_type: with specific word_type
        @return: Get LearningSet from cash or if it's not in a cash from DB
        """
        learning_set = RedisImplementation.get_learning_set(user_name)
        if not learning_set:
            # Get information from DB
            # TODO CRIT: Maybe Here get just words without any other logic?
            learning_set = ProcessService.start_learning_process(user_name, word_type)
        return learning_set

    @staticmethod
    def add_learning_set_to_cash(learning_set: LearningSet) -> None:
        """
        Add learning set to Redis
        @param learning_set: learning_set which you want to cash
        @return: None
        """
        # Put information from Radis
        RedisImplementation.add_learning_set(learning_set)

    @staticmethod
    def start_learning_process(user_name: str, word_type: WordTypeEnum) -> LearningSet:
        """
        Start learning process with creating learning set
        @param user_name: user_name for which learning_set will be created
        @param word_type: word type used for selecting type of learning set (standard or custom)
        @return: LearningSet
        """
        # If it's working with standard words
        if word_type == WordTypeEnum.standard:
            learning_set = ProcessService.start_standard_learning_process(user_name)
            return learning_set
        else:
            # Custom and all another
            learning_set = ProcessService.start_custom_learning_process(user_name, word_type)
            return learning_set

    @staticmethod
    def start_custom_learning_process(user_name: str, word_type: WordTypeEnum = WordTypeEnum.custom) -> LearningSet:
        """
        Start custom learning process. With words, which user created before
        @param user_name: for user with this user_name
        @param word_type: with custom word_type
        @return: LearningSet
        """
        # Get information from DB
        user = UserOrm.find_user_by_name(user_name)
        if not user:
            raise ValueError(f"User with name {user_name} wasn't found")
        words_list = WordOrm.find_words_by_user_id(user_id=user.id, training_length=user.training_length,
                                                   word_type=word_type)
        if not words_list:
            raise ValueError(f"Words for user with name {user_name} wasn't found")
        learning_set = LearningSet(user, words_list)
        ProcessService.add_learning_set_to_cash(learning_set)
        return learning_set

    def start_standard_learning_process(user_name: str) -> LearningSet:
        """
        Start learning process with Words which created by system
        @param word_type: standard
        @return:LearningSet
        """
        word_type = WordTypeEnum.standard
        # Get information from DB
        user = UserOrm.find_user_by_name(user_name)
        if not user:
            raise ValueError(f"User with name {user_name} wasn't found")

        # Try to get N percent of words which was trained
        existed_words_amount = user.training_length - int(Constant.PERCENT_NEW_WORDS_IN_SET*user.training_length)
        trained_list = WordOrm.find_words_for_standard_type(user.id, existed_words_amount, word_type)

        new_amount = user.training_length - len(trained_list)
        if new_amount > 0:
            # Get other words from Word
            new_words_list = WordOrm.find_new_words_for_standard_type(training_length=new_amount)
            # Add information about neq words to StandardWordUser
            new_word_user_list = [StandardWordDTO(
                id=uuid.uuid4(),
                user_id=user.id,
                amount_already_know=0,
                amount_back_to_learning=0,
                word_id=word.id
            ) for word in new_words_list]

            if new_word_user_list:
                # TODO: NEED TO DO THIS IN QUEUE
                StandardWordUserOrm.create_list_new_words(new_word_user_list)

            # Get list of combination (word which already was trained) + (new standard words)
            words_list = trained_list + new_words_list
        else:
            words_list = trained_list

        if not words_list:
            raise ValueError(f"Words for user with name {user_name} wasn't found")
        learning_set = LearningSet(user, words_list)
        ProcessService.add_learning_set_to_cash(learning_set)
        return learning_set

    @staticmethod
    def update_learning_progress(user_id: uuid.UUID, word_id: uuid.UUID, german_word: str, user_action: UserActionEnum,
                                 word_type: WordTypeEnum) -> None:
        """
        Depend on the learning process update different parameters
        @param user_id: for user with user_id
        @param word_id: for word with word_id
        @param german_word: for word with meaning german_word
        @param user_action: type of user_action
        @param word_type: User process selected by this parameter (word_type)
        @return: None
        """
        # Depends of type of word, update different tables
        if (word_type == WordTypeEnum.custom):
            ProcessService.update_custom_learning_progress(user_id, german_word, user_action)
        else:
            ProcessService.update_standard_learning_progress(user_id, word_id, user_action)
    @staticmethod
    def update_custom_learning_progress(user_id: uuid.UUID, german_word: str, user_action: UserActionEnum) -> None:
        """
        Update custom amount for user in table Word
        @param user_id: user_id
        @param user_action: user_action
        @return: None
        """
        # Set up counter by flags
        if user_action == UserActionEnum.ALREADY_KNOW:
            inc_amount_already_know = 1
            inc_amount_back_to_learning = 0
        else:
            inc_amount_already_know = 0
            inc_amount_back_to_learning = 1

        # TODO: ADD Queue here
        WordOrm.update_counter_for_word(german_word, user_id, inc_amount_already_know, inc_amount_back_to_learning)

    @staticmethod
    def update_standard_learning_progress(user_id: uuid.UUID, word_id: uuid.UUID, user_action: UserActionEnum):
        """
        Update standard amount for user in table StandardWordUser
        @param user_name: user_name
        @param german_word: german_word
        @param user_action: user_action
        @return: None
        """
        # Set up counter by flags
        if user_action == UserActionEnum.ALREADY_KNOW:
            inc_amount_already_know = 1
            inc_amount_back_to_learning = 0
        else:
            inc_amount_already_know = 0
            inc_amount_back_to_learning = 1

        # TODO: ADD Queue here
        StandardWordUserOrm.update_counter_for_word(word_id, user_id, inc_amount_already_know, inc_amount_back_to_learning)
