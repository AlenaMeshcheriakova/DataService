from sqlalchemy.orm import Mapped, mapped_column

from src.model.level_enum import LevelEnum
from src.db.base import Base

class Level(Base):
    __tablename__ = "lang_level"

    id: Mapped[Base.get_intpk(self=Base)]
    lang_level: Mapped[str] = mapped_column(unique=True, nullable=False)
    created_at: Mapped[Base.get_created_at(self=Base)]
    updated_at: Mapped[Base.get_updated_at(self=Base)]

    def get_id(self):
        return self.id

    def get_lang_level(self):
        return self.lang_level

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}