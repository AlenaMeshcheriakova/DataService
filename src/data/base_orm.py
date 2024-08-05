
from src.db.database import sync_engine
from src.db.base import Base
class BaseOrm:

    @staticmethod
    def create_tables():
        sync_engine.echo = False
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
        sync_engine.echo = True
