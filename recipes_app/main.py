from typing import List
import uvicorn

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from CRUD.database import engine, create_table, async_session
from CRUD.db_recipes import get_all_recipes, creat_new_recipe, get_id_recipe, update_number_view
from core import models, schemas
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, HTTPException, status, Depends
from contextlib import asynccontextmanager
from typing import AsyncGenerator


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session.begin() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise
        finally:
            await session.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_table()
    yield

app = FastAPI(lifespan=lifespan)


@app.post('/recipes/',
          response_model=schemas.RecipeCreate,
          status_code=status.HTTP_201_CREATED, )
async def create_recipe(recipe: schemas.RecipeCreate, session=Depends(get_async_session)) -> models.Recipe:
    """create new recipe"""
    new_recipe = await creat_new_recipe(session=session, recipe_create=recipe)
    return jsonable_encoder(new_recipe)


@app.get('/recipes/', response_model=List[schemas.RecipeReadAll])
async def get_recipes(session=Depends(get_async_session)) -> List[models.Recipe]:
    """get all recipes"""
    recipes = await get_all_recipes(session=session)
    return recipes


@app.get('/recipes/{recipe_id}', response_model=schemas.RecipeRead)
async def get_recipe(recipe_id: int, session=Depends(get_async_session)) -> models.Recipe:
    """
    get recipe by id

    """
    recipe = await get_id_recipe(session=session, recipe_id=recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Id not found")
    else:
        recipe = await update_number_view(session=session, recipe=recipe)
        return jsonable_encoder(recipe)


@app.get("/")
async def root():
    return {"message": "Tomato"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app", reload=True)
