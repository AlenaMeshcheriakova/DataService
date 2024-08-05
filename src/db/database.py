from typing import AsyncGenerator

from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from src.model.userdb import UserDB
from cfg.сonfig import settings
from fastapi import Depends

# --------------------WORK WITH ENGINE--------------------

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,
    pool_size=15,
    # max_overflow=10
)

session_factory = sessionmaker(sync_engine)

def get_session():
    with session_factory() as session:
        yield session

# ---------------CREATE AND DELETE ALL---------------
# async def create_db_and_tables():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
# async def delete_tables():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
