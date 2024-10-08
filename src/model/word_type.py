from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base

class WordType(Base):
    __tablename__ = "word_type"

    id: Mapped[Base.get_intpk(self=Base)]
    word_type: Mapped[str] = mapped_column(unique=True, nullable=False)
    created_at: Mapped[Base.get_created_at(self=Base)]
    updated_at: Mapped[Base.get_updated_at(self=Base)]

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}