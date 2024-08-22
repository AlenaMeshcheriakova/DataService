import uuid

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base

class UserDB(Base):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}

    id: Mapped[Base.get_intpk(self=Base)]
    auth_user_id: Mapped[uuid.UUID] = mapped_column(unique=True, nullable=True)

    user_name: Mapped[str] = mapped_column(unique=True)
    training_length: Mapped[int] = mapped_column( default=10, nullable=True)
    created_at: Mapped[Base.get_created_at(self=Base)]
    updated_at: Mapped[Base.get_updated_at(self=Base)]

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}