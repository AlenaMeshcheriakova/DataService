import uuid
from unittest.mock import MagicMock

import pytest

from sqlalchemy import insert

from src.model.group import Group
from src.model.level import Level
from src.model.level_enum import LevelEnum
from src.db.database import session_factory
from src.dto.schema import LevelAddDTO, WordTypeAddDTO
from src.model.userdb import UserDB
from src.model.word_type import WordType
from src.model.word_type_enum import WordTypeEnum
from src.model.word import Word


# --------------------TEST CONSTANT--------------------
class DataPreparation:

    TEST_USER_ID = uuid.uuid4()
    TEST_USER_NAME = 'TEST_USER_NAME'
    TEST_USER_EMAIL = 'TEST_USER_EMAIL@gmail.com'
    TEST_PASS = 'TEST_PASS'
    TEST_TELEGRAM_USER_ID = "12341234"

    # Group
    TEST_GROUP_NAME = 'TEST_GROUP_NAME'
    TEST_GROUP_ID = uuid.uuid4()

    TEST_COMMON_GROUP_NAME = 'CUSTOM_GROUP'
    TEST_COMMON_GROUP_ID = uuid.uuid4()

    # Level
    TEST_LEVEL_NAME = LevelEnum.a1
    TEST_LEVEL_ID = uuid.uuid4()

    # Word type
    TEST_WORD_TYPE = WordTypeEnum.test
    TEST_CUSTOM_WORD_TYPE = WordTypeEnum.custom
    TEST_WORD_TYPE_ID = uuid.uuid4()
    TEST_CUSTOM_WORD_TYPE_ID = uuid.uuid4()

    # Word
    TEST_WORD_DICT = [
        {'german_word' : "Hallo",
         'english_word': "Hello",
         'russian_word': "Привет"},
        {'german_word': "beantragen",
         'english_word': "apply for",
         'russian_word': "предлагать"},
        {'german_word': "der Antrag",
         'english_word': "request",
         'russian_word': "Предложение"},
        {'german_word': "einzahlen",
         'english_word': "pay",
         'russian_word': "платить"},
        {'german_word': "die Einzahlung",
         'english_word': "Deposit",
         'russian_word': "взнос,оплата"},
        {'german_word': "verdienen",
         'english_word': "earn",
         'russian_word': "зарабатывать"},
        {'german_word': "überweisen",
         'english_word': "transfer",
         'russian_word': "переводить деньги"},
        {'german_word': "wechseln",
         'english_word': "change",
         'russian_word': "менять, обменивать"},
        {'german_word': "sperren",
         'english_word': "block, lock out",
         'russian_word': "закрывать,блокировать"},
        {'german_word': "der Wechsel",
         'english_word': "the change",
         'russian_word': "изменение"},
        {'german_word': "die überweisung",
         'english_word': "the transfer",
         'russian_word': "перевод денег"},
        {'german_word': "der Verdienst",
         'english_word': "income",
         'russian_word': "заработок, заслуга"}
    ]

    TEST_WORD_DICT_MINI = [
        {'german_word': "Hallo",
         'english_word': "Hello",
         'russian_word': "Привет"},
        {'german_word': "beantragen",
         'english_word': "apply for",
         'russian_word': "предлагать"},
        {'german_word': "der Antrag",
         'english_word': "request",
         'russian_word': "Предложение"}
    ]

    TEST_WORD = {'german_word': "Hallo",
         'english_word': "Hello",
         'russian_word': "Привет"}

# --------------------Mock--------------------

@pytest.fixture
def mock_bot():
    """Fixture to create a mock bot."""
    mock_bot = MagicMock()
    # Mock message_handler to simulate registering handlers
    mock_bot.message_handler = MagicMock()
    return mock_bot


# --------------------FIXTURE--------------------

@pytest.fixture()
def create_test_user():
    """Create Test User in the beginning of  tests
    """
    with session_factory() as session:
        new_user = UserDB(
            id = DataPreparation.TEST_USER_ID,
            user_name= DataPreparation.TEST_USER_NAME,
            training_length=10,
            email= DataPreparation.TEST_USER_EMAIL,
            hashed_password= DataPreparation.TEST_PASS,
            is_active=True,
            telegram_user_id= DataPreparation.TEST_TELEGRAM_USER_ID
        )
        session.add(new_user)
        session.commit()

@pytest.fixture()
def create_all_levels_for_test():
    """Create levels by LevelEnum for tests """
    with session_factory() as session:
        for level in LevelEnum:
            new_level = LevelAddDTO(lang_level=level, id=uuid.uuid4())
            stmt = insert(Level).values(**new_level.dict())
            session.execute(stmt)
        session.commit()

@pytest.fixture()
def create_test_level():
    """Create test level by TEST_LEVEL_NAME with id=TEST_LEVEL_ID """
    with session_factory() as session:
        new_level = LevelAddDTO(lang_level=DataPreparation.TEST_LEVEL_NAME, id=DataPreparation.TEST_LEVEL_ID)
        stmt = insert(Level).values(**new_level.dict())
        session.execute(stmt)
        session.commit()


@pytest.fixture()
def create_test_group():
    """Create test group for tests """
    with session_factory() as session:
        stmt = insert(Group).values(**{
            'id': DataPreparation.TEST_GROUP_ID,
            'group_name': DataPreparation.TEST_GROUP_NAME,
            'user_id': DataPreparation.TEST_USER_ID
        })
        session.execute(stmt)
        session.commit()
    """Create test group for tests - COMMON """
    with session_factory() as session:
        stmt = insert(Group).values(**{
            'id': DataPreparation.TEST_COMMON_GROUP_ID,
            'group_name': DataPreparation.TEST_COMMON_GROUP_NAME,
            'user_id': DataPreparation.TEST_USER_ID
        })
        session.execute(stmt)
        session.commit()

@pytest.fixture()
def create_test_word_type():
    """Create tests word typy """
    # Create TEST TYPE
    with session_factory() as session:
        wt_dto = WordTypeAddDTO(word_type=DataPreparation.TEST_WORD_TYPE, id=DataPreparation.TEST_WORD_TYPE_ID)
        stmt = insert(WordType).values(**wt_dto.dict())
        session.execute(stmt)
        session.commit()
    # Create CUSTOM
    with session_factory() as session:
        wt_dto = WordTypeAddDTO(word_type=DataPreparation.TEST_CUSTOM_WORD_TYPE, id=DataPreparation.TEST_CUSTOM_WORD_TYPE_ID)
        stmt = insert(WordType).values(**wt_dto.dict())
        session.execute(stmt)
        session.commit()

@pytest.fixture()
def create_list_test_words():
    """Create tests word typy """
    with session_factory() as session:
        for word in DataPreparation.TEST_WORD_DICT:
            stmt = insert(Word).values(**{
                'id': uuid.uuid4(),
                'german_word': word.get('german_word'),
                'english_word': word.get('english_word'),
                'russian_word': word.get('russian_word'),
                'lang_level_id': DataPreparation.TEST_LEVEL_ID,
                'word_type_id': DataPreparation.TEST_WORD_TYPE_ID,
                'group_id': DataPreparation.TEST_GROUP_ID,
                'user_id': DataPreparation.TEST_USER_ID,
                'amount_already_know': 0,
                'amount_back_to_learning': 0
            })
            session.execute(stmt)
        session.commit()

@pytest.fixture()
def create_mini_list_test_words():
    """Create tests word typy """
    with session_factory() as session:
        for word in DataPreparation.TEST_WORD_DICT_MINI:
            stmt = insert(Word).values(**{
                'id': uuid.uuid4(),
                'german_word': word.get('german_word'),
                'english_word': word.get('english_word'),
                'russian_word': word.get('russian_word'),
                'lang_level_id': DataPreparation.TEST_LEVEL_ID,
                'word_type_id': DataPreparation.TEST_WORD_TYPE_ID,
                'group_id': DataPreparation.TEST_GROUP_ID,
                'user_id': DataPreparation.TEST_USER_ID,
                'amount_already_know': 0,
                'amount_back_to_learning': 0
            })
            session.execute(stmt)
        session.commit()

@pytest.fixture()
def create_test_word():
    """Create one test word  """
    test_word_id = uuid.uuid4()
    word = DataPreparation.TEST_WORD
    with session_factory() as session:
        stmt = insert(Word).values(**{
            'id': test_word_id,
            'german_word': word.get('german_word'),
            'english_word': word.get('english_word'),
            'russian_word': word.get('russian_word'),
            'lang_level_id': DataPreparation.TEST_LEVEL_ID,
            'word_type_id': DataPreparation.TEST_WORD_TYPE_ID,
            'group_id': DataPreparation.TEST_GROUP_ID,
            'user_id': DataPreparation.TEST_USER_ID,
            'amount_already_know': 0,
            'amount_back_to_learning': 0
        })
        session.execute(stmt)
        session.commit()
