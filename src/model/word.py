from typing import Optional

from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


class Word(Base):
    __tablename__ = "word"

    id: Mapped[Base.get_intpk(self=Base)]
    german_word: Mapped[str] = mapped_column(String[256])
    english_word: Mapped[Optional[str]] = mapped_column(String[256], nullable=True)
    russian_word: Mapped[str] = mapped_column(String[256])

    lang_level_id: Mapped[int] = mapped_column(ForeignKey("lang_level.id", ondelete="NO ACTION"))
    word_type_id: Mapped[int] = mapped_column(ForeignKey("word_type.id", ondelete="NO ACTION"))
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id", ondelete="NO ACTION"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    amount_already_know: Mapped[int]
    amount_back_to_learning: Mapped[int]

    created_at: Mapped[Base.get_created_at(self=Base)]
    updated_at: Mapped[Base.get_updated_at(self=Base)]

    user: Mapped["src.model.userdb.UserDB"] = relationship(
        # back_populates="words"
    )

    __table_args__ = (
        UniqueConstraint('german_word', 'user_id', name='uq_german_word_user_id'),
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}