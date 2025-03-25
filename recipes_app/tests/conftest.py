from typing import AsyncGenerator
from fastapi.testclient import TestClient
from recipes_app.main import app, get_async_session

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import insert, select
from recipes_app.core.models import Recipe
from sqlalchemy.orm import Session
from recipes_app.CRUD.database import Base


DATABASE_URL_TEST = "sqlite+aiosqlite:///testdb.db"

engine_test = create_async_engine(url=DATABASE_URL_TEST, echo=True, )
async_session_test = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_test() as session_test:
        yield session_test

app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def async_db_engine():
    async with engine_test.begin() as conn:
        print("CREATE DB")
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        print("DROP DB")
        await conn.run_sync(Base.metadata.drop_all)

# @pytest.fixture(scope='session')
# async def async_client() -> AsyncClient:
#     return AsyncClient(app=app, base_url='http://test')


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app),base_url='http://test') as ac:
        yield ac


# SETUP
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


async def add_recipe():
    with AsyncSession(engine_test) as sess:
        recipe = Recipe(title="Яйчница", cooking_time=5,
                        text="Разбить яйца на горячую сковороду. Посолить. Добавить зелень и помидоры.",
                        ingredients_list="Яйца, укроп, соль, томаты")
        sess.add(recipe)
        sess.commit()
