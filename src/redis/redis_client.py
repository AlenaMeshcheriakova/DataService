
import json
from typing import Optional, Union
import redis

from UUIDEncoder import UUIDEncoder
from src.dto.learning_set import LearningSet
from src.redis.redis_const import RedisConstant


class RedisImplementation:

    _instance: Optional[redis.Redis] = None

    def __init__(self, host='localhost', port=6379, decode_responses=True):
        if RedisImplementation._instance is None:
            RedisImplementation._instance = redis.Redis(host=host, port=port, decode_responses=decode_responses)

    @classmethod
    def get_instance(cls) -> redis.Redis:
        if cls._instance is None:
            raise Exception("RedisClient not initialized. Call the constructor first.")
        return cls._instance

    @classmethod
    def add_learning_set(cls, learning_set: LearningSet) -> None:
        """
        Add current learning set to the cash
        @param learning_set: learning set
        @return: None
        """
        r = cls._instance
        key = RedisConstant.REDIS_USER_NAME + learning_set.user.user_name + ':' + RedisConstant.REDIS_LEARNING_SET
        json_images = json.dumps(learning_set.json())
        r.set(key, json_images, RedisConstant.REDIS_TIME_EXPIRED)


    @classmethod
    def get_learning_set(cls, user_name) -> Union[LearningSet|None]:
        """
        Get training length parameter by user from Radis
        @param user_name: user_name
        @return: Training Length
        """
        r = cls._instance
        key = RedisConstant.REDIS_USER_NAME + user_name + ':' + RedisConstant.REDIS_LEARNING_SET
        # Read saved JSON str from Redis and unpack into python dict
        data = r.get(key)
        if data:
            learning_set_data = json.loads(data)
            retrieved_learning_set = LearningSet.from_json(learning_set_data)
            return retrieved_learning_set
        else:
            return None

    @classmethod
    def add_training_length_to_user(cls, user_name, cashed_training_length) -> None:
        """
        Add amount of training set for user
        @return: None
        """
        # Add amount of words
        r = cls._instance
        key = RedisConstant.REDIS_USER_NAME + user_name + ':' + RedisConstant.REDIS_TOTAL_AMOUNT
        json_images = json.dumps(cashed_training_length)
        r.set(key, json_images, RedisConstant.REDIS_TIME_EXPIRED)

    @classmethod
    def add_position_in_training_set(cls, user_name, learning_position) -> None:
        """
        Add current position in training set ro cash
        @param user_name: user_name
        @param learning_position: current learning position
        @return: None
        """
        r = cls._instance
        key = RedisConstant.REDIS_USER_NAME + user_name + ':' + RedisConstant.REDIS_CURRENT_POSITION
        json_images = json.dumps(learning_position)
        r.set(key, json_images, RedisConstant.REDIS_TIME_EXPIRED)

    @classmethod
    def add_words_by_user(cls, user_name, words_list) -> None:
        """
        Add lists of words
        @param user_name: user_name
        @param words_list: Training set
        @return: None
        """
        r = cls._instance
        key = RedisConstant.REDIS_USER_NAME + user_name + ':' + RedisConstant.REDIS_LIST
        for word in words_list:
            # Convert python dict to JSON str and save to Redis
            json_images = json.dumps(word.as_dict(), cls=UUIDEncoder)
            r.rpush(key, json_images)

    @classmethod
    def get_words_by_user(cls, user_name):
        """
        Get a list of words for user
        @param user_name: user_name
        @return: List of Words
        """
        r = cls._instance
        key = RedisConstant.REDIS_USER_NAME + user_name + ':' + RedisConstant.REDIS_LIST
        # Read saved JSON str from Redis and unpack into python dict
        getted_words = r.lpop(key)
        return getted_words

    @classmethod
    def get_training_length(cls, user_name) -> int:
        """
        Get training length parameter by user from Radis
        @param user_name: user_name
        @return: Training Length
        """
        r = cls._instance
        key = RedisConstant.REDIS_USER_NAME + user_name + ':' + RedisConstant.REDIS_TOTAL_AMOUNT
        # Read saved JSON str from Redis and unpack into python dict
        return int(r.get(key))

    @classmethod
    def get_current_position(cls, user_name):
        """
        Get current position  by user from Radis
        @param user_name: user_name
        @return: Current position in training set
        """
        r = cls._instance
        key = RedisConstant.REDIS_USER_NAME + user_name + ':' + RedisConstant.REDIS_CURRENT_POSITION
        # Read saved JSON str from Redis and unpack into python dict
        return int(r.get(key))

    @classmethod
    def inc_current_position(cls, user_name) -> None:
        """
        Increment current position (Go to next word)
        @param user_name: user_name
        @return: None
        """
        r = cls._instance
        key = RedisConstant.REDIS_USER_NAME + user_name + ':' + RedisConstant.REDIS_CURRENT_POSITION
        new_current_amount = cls.get_current_position(user_name) + 1
        json_images = json.dumps(new_current_amount)
        r.set(key, json_images, RedisConstant.REDIS_TIME_EXPIRED)


    @classmethod
    def get_current_word(cls, user_name):
        r = cls._instance
        key_current_pos = RedisConstant.REDIS_USER_NAME + user_name + ':' + RedisConstant.REDIS_CURRENT_WORD
        # push word to current position field
        current_word = json.loads(r.get(key_current_pos))
        return current_word

    @classmethod
    def update_current_word(cls, user_name, next_word) -> None:
        """
        Update current learning word to next one (next_word)
        @param user_name: user_name
        @param next_word: next_word
        @return: None
        """
        r = cls._instance
        # Put getting word to current word state
        key_current_pos = RedisConstant.REDIS_USER_NAME + user_name + ':' + RedisConstant.REDIS_CURRENT_WORD
        # push word to current position field
        json_images = json.dumps(next_word)
        r.set(key_current_pos, json_images, RedisConstant.REDIS_TIME_EXPIRED)