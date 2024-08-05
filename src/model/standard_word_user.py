from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base

class StandardWordUser(Base):
    __tablename__ = "standard_word_user"

    id: Mapped[Base.get_intpk(self=Base)]

    word_id: Mapped[int] = mapped_column(ForeignKey("word.id", ondelete="NO ACTION"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    amount_already_know: Mapped[int]
    amount_back_to_learning: Mapped[int]

    created_at: Mapped[Base.get_created_at(self=Base)]
    updated_at: Mapped[Base.get_updated_at(self=Base)]

    __table_args__ = (
        UniqueConstraint('word_id', 'user_id', name='uq_word_id_user_id'),
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}