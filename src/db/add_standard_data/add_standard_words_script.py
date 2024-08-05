import sys
import uuid
import csv

from src.dto.schema import UserCreateTelegramDTO, GroupAddDTO
from src.service.group_word_service import GroupWordService
from src.service.user_service import UserService
from src.service.word_service import WordService
from word_type_enum import WordTypeEnum

# DIDN'T CHANGE IT, IT'S STANDARD USER
STANDARD_USER_NAME = "STANDARD_USER"
standard_user_id = uuid.uuid4()
STANDARD_GROUP_NAME = "STANDARD_GROUP"
standard_group_id = uuid.uuid4()


def create_standard_user():
    """
    User for all the standards word which can be used by different Users
    @return:
    """
    # Check that standard user was created
    user = UserService.is_user_created(STANDARD_USER_NAME)
    global standard_user_id
    if not user:
        # If user wasn't created
        new_user_dto = UserCreateTelegramDTO(
            id=standard_user_id,
            user_name=STANDARD_USER_NAME,
            training_length=10,
            telegram_user_id="123123",
            hashed_password="123123",
            email="standard@standars.com"
        )
        UserService.create_user_by_DTO(new_user_dto)
    else:
        standard_user_id = UserService.get_user_by_name(STANDARD_USER_NAME).id

def create_standard_group():
    """
    User for all the standards word which can be used by different Users
    @return:
    """
    # Check that standard group was created
    is_group = GroupWordService.is_group_created(STANDARD_GROUP_NAME)
    global standard_group_id
    if not is_group:
        # Create standard group
        GroupWordService.create_group(GroupAddDTO(
            id=standard_group_id,
            group_name=STANDARD_GROUP_NAME,
            user_id=standard_user_id
        ))
    else:
        standard_group_id = GroupWordService.get_group_id_by_group_name(STANDARD_GROUP_NAME)

def read_words_from_csv(file_path):
    words = []
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            words.append({
                'german_word': row['german_word'],
                'english_word': row['english_word'],
                'russian_word': row['russian_word'],
                'level': row['level']
            })
    return words

def main():
    create_standard_user()
    create_standard_group()
    words = read_words_from_csv("addding_words.csv")
    for word in words:
        WordService.add_new_word(STANDARD_USER_NAME, word.get('german_word'), word.get('english_word'), word.get('russian_word'),
                                 0, 0,
                                 group_word_name=STANDARD_GROUP_NAME, level=word.get('level'),
                                 word_type=WordTypeEnum.standard)

if __name__ == "__main__":
    sys.exit(main())