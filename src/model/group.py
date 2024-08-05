from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base

class Group(Base):
    """
    Object class Group - represent group of words, which user can create and grouped by group name
    Only one group with unique name can be created for one user
    (Can be different group with the same name for different user)
    """
    __tablename__ = "group"

    id: Mapped[Base.get_intpk(self=Base)]
    group_name: Mapped[str] = mapped_column(String[256])
    created_at: Mapped[Base.get_created_at(self=Base)]
    updated_at: Mapped[Base.get_updated_at(self=Base)]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))

    __table_args__ = (
        UniqueConstraint('group_name', 'user_id', name='uq_group_name_user_id'),
    )

