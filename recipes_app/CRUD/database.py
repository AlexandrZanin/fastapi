from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy import MetaData

DATABASE_URL = "sqlite+aiosqlite:///./recipes.db"


async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)
session = async_session()


class Base(DeclarativeBase):

    id: Mapped[int] = mapped_column(primary_key=True)


metadata = MetaData()
