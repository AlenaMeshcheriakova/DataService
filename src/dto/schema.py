import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, RootModel
from fastapi_users import schemas

from src.model.level import LevelEnum
from src.model.word_type_enum import WordTypeEnum


#---------------------User---------------------

class UserDTO(schemas.BaseUser):
    # id: uuid.UUID
    user_name: str = Field(max_length=35)
    training_length: int = Field(ge=0)
    created_at: datetime
    updated_at: datetime

class UserDTOUpdate(schemas.BaseUser):
    user_name: str = Field(max_length=35)
    training_length: int = Field(ge=0)
    created_at: datetime
    updated_at: datetime

class UserCreateDTO(schemas.BaseUser):
    user_name: str = Field(max_length=35)
    training_length: int = Field(ge=0)

class UserCreateTelegramDTO(schemas.BaseUser):
    id: uuid.UUID
    user_name: str = Field(max_length=35)
    training_length: int = Field(ge=0)
    telegram_user_id: str = Field(max_length=35)
    hashed_password: Optional[str] = None
    email: Optional[EmailStr] = None

class UserCreateFullDTO(schemas.BaseUser):
    id: uuid.UUID
    user_name: str = Field(max_length=35)
    telegram_user_id: str = Field(max_length=35)
    training_length: int = Field(ge=0)
    created_at: datetime
    updated_at: datetime
    password: Optional[str] = None
    hashed_password: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None

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
    created_at: datetime
    updated_at: datetime

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
    lang_level: LevelEnum

class LevelDTO(BaseModel):
    lang_level: LevelEnum
    created_at: datetime
    updated_at: datetime

class LevelList(RootModel):
    root: List[LevelDTO]

#---------------------WordType---------------------

class WordTypeAddDTO(BaseModel):
    id: uuid.UUID
    word_type: WordTypeEnum

class WordTypeDTO(BaseModel):
    word_type: WordTypeEnum
    created_at: datetime
    updated_at: datetime

class WordTypeList(RootModel):
    root: List[WordTypeDTO]