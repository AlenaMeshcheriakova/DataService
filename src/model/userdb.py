from typing import List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from pydantic import Field
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.model.word import Word
from src.db.base import Base

class UserDB(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}

    id: Mapped[Base.get_intpk(self=Base)]

    telegram_user_id: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column( default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column( default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)

    user_name: Mapped[str] = mapped_column(unique=True)
    training_length: Mapped[int] = mapped_column( default=10, nullable=True)
    created_at: Mapped[Base.get_created_at(self=Base)]
    updated_at: Mapped[Base.get_updated_at(self=Base)]

    # words: Mapped[List["Word"]] = relationship(
    #     back_populates="user"
    # )
