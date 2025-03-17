import pytest
from fastapi.testclient import TestClient

from main import app
from CRUD.database import metadata, session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool
from sqlalchemy import create_engine

DATABASE_URL_TEST = "sqlite+aiosqlite:///testdb.db"

engine_test = create_engine(DATABASE_URL_TEST, poolclass=NullPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)
metadata.bind = engine_test

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
# @pytest.mark.anyio
async def test_root():
    # async with client as ac:
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Tomato"}


async def test_get_recipe_id():
    # async with client as ac:
    response = await client.get("/recipes/1")
    assert response.status_code == 200
