import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, RootModel, EmailStr


# ---------------------AUTH---------------------
class UserResponse(BaseModel):
    username: str
    message: str

class RegisterRequest(BaseModel):
    username: str
    password: str
    email: EmailStr
    telegram_user_id: str

#---------------------User---------------------

class UserDTO(BaseModel):
    auth_user_id: Optional[uuid.UUID]
    user_name: str = Field(max_length=35)
    training_length: int = Field(ge=0)
    created_at: datetime
    updated_at: datetime

class UserDTOUpdate(BaseModel):
    auth_user_id: Optional[uuid.UUID] = None
    user_name: str = Field(max_length=35)
    training_length: int = Field(ge=0)
    created_at: datetime
    updated_at: datetime

class UserCreateDTO(BaseModel):
    auth_user_id: Optional[uuid.UUID] = None
    user_name: str = Field(max_length=35)
    training_length: int = Field(ge=0)

class UserCreateTelegramDTO(BaseModel):
    id: uuid.UUID
    auth_user_id: Optional[uuid.UUID] = None
    user_name: str = Field(max_length=35)
    training_length: int = Field(ge=0)

class UserAuthTelegramDTO(BaseModel):
    id: uuid.UUID
    auth_user_id: Optional[uuid.UUID] = None
    user_name: str = Field(max_length=35)
    training_length: int = Field(ge=0)
    password: str
    email: EmailStr
    telegram_user_id: str

class UserCreateFullDTO(BaseModel):
    id: uuid.UUID
    user_name: str = Field(max_length=35)
    training_length: int = Field(ge=0)
    auth_user_id: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime

#---------------------Word---------------------
class WordAddDTO(BaseModel):
    user_id: uuid.UUID
    german_word: str = Field(max_length=63)
    english_word: Optional[str] = Field(max_length=45)
    russian_word: Optional[str] = Field(max_length=33)
    amount_already_know: int = Field(ge=0)
    amount_back_to_learning: int = Field(ge=0)
    lang_level_id: uuid.UUID
    word_type_id: uuid.UUID
    group_id: uuid.UUID

class WordDTO(WordAddDTO):
    id: uuid.UUID
    # created_at: datetime
    # updated_at: datetime

class WordGetDTO(BaseModel):
    user_id: uuid.UUID
    german_word: str = Field(max_length=63)
    english_word: Optional[str] = Field(max_length=45)
    russian_word: Optional[str] = Field(max_length=33)
    amount_already_know: int = Field(ge=0)
    amount_back_to_learning: int = Field(ge=0)
    lang_level_id: uuid.UUID
    word_type_id: uuid.UUID
    group_id: uuid.UUID


def convert_word_dto_to_word_get_dto(training_set: List[WordDTO]) -> List[WordGetDTO]:
    return [
        WordGetDTO(
            user_id=word.user_id,
            german_word=word.german_word,
            english_word=word.english_word,
            russian_word=word.russian_word,
            amount_already_know=word.amount_already_know,
            amount_back_to_learning=word.amount_back_to_learning,
            lang_level_id=word.lang_level_id,
            word_type_id=word.word_type_id,
            group_id=word.group_id
        )
        for word in training_set
    ]

#---------------------StandardWordUser---------------------
class StandardWordAddDTO(BaseModel):
    user_id: uuid.UUID
    amount_already_know: int = Field(ge=0)
    amount_back_to_learning: int = Field(ge=0)
    word_id: uuid.UUID

class StandardWordDTO(StandardWordAddDTO):
    id: uuid.UUID
    # created_at: datetime
    # updated_at: datetime

class StandardWordGetDTO(BaseModel):
    user_id: uuid.UUID
    amount_already_know: int = Field(ge=0)
    amount_back_to_learning: int = Field(ge=0)
    word_id: uuid.UUID


#---------------------Group---------------------
class GroupAddDTO(BaseModel):
    id: uuid.UUID
    group_name: str = Field(max_length=256)
    user_id: uuid.UUID

class GroupDTO(GroupAddDTO):
    created_at: datetime
    updated_at: datetime

class GroupList(RootModel):
    root: List[GroupDTO]

#---------------------Level---------------------

class LevelAddDTO(BaseModel):
    id: uuid.UUID
    lang_level: str = Field(max_length=256)

class LevelDTO(BaseModel):
    lang_level: str = Field(max_length=256)
    created_at: datetime
    updated_at: datetime

class LevelFullDTO(LevelAddDTO):
    created_at: datetime
    updated_at: datetime

class LevelList(RootModel):
    root: List[LevelDTO]

def convert_full_level_dto_to_level_dto(level: LevelFullDTO) -> LevelDTO:
    return LevelDTO(
        lang_level=level.lang_level,
        created_at=level.created_at,
        updated_at=level.updated_at
    )

#---------------------WordType---------------------

class WordTypeAddDTO(BaseModel):
    id: uuid.UUID
    word_type: str = Field(max_length=256)

class WordTypeDTO(BaseModel):
    word_type: str = Field(max_length=256)
    created_at: datetime
    updated_at: datetime

class WordTypeList(RootModel):
    root: List[WordTypeDTO]