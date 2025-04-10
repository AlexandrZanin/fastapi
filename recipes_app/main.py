from contextlib import asynccontextmanager
from typing import AsyncGenerator, List, Any, Sequence

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from .core import models, schemas
from .CRUD.database import async_session, create_table
from .CRUD.db_recipes import (
    creat_new_recipe,
    get_all_recipes,
    get_id_recipe,
    update_number_view,
    update_recipes,
)
from .core.models import Recipe


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session.begin() as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_table()
    yield


app = FastAPI(lifespan=lifespan)


@app.post(
    "/recipes/",
    response_model=schemas.RecipeCreate,
    status_code=status.HTTP_201_CREATED,
)
async def create_recipe(
    recipe: schemas.RecipeCreate, session=Depends(get_async_session)
) -> models.Recipe:
    """create new recipe"""
    new_recipe = await creat_new_recipe(session=session, recipe_create=recipe)
    return jsonable_encoder(new_recipe)


@app.get("/recipes/", response_model=List[schemas.RecipeReadAll])
async def get_recipes(session=Depends(get_async_session)) -> Sequence[Any]:
    """get all recipes"""
    return await get_all_recipes(session=session)


@app.get("/recipes/{recipe_id}", response_model=schemas.RecipeRead)
async def get_recipe(
    recipe_id: int, session=Depends(get_async_session)
) -> models.Recipe:
    """
    get recipe by id

    """
    recipe = await get_id_recipe(session=session, recipe_id=recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Id not found")
    else:
        recipe = await update_number_view(session=session, recipe=recipe)
        return jsonable_encoder(recipe)


@app.put("/recipes/{recipe_id}")
async def update_recipe(
    recipe_id: int,
    recipe: schemas.RecipeUpdate,
    session=Depends(get_async_session),
):
    """
    update recipe
    """
    db_recipe: Recipe | None = await (get_id_recipe
                                      (session=session, recipe_id=recipe_id))
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Id not found")
    new_recipe = await update_recipes(
        session=session, recipe_update=recipe, db_recipe=db_recipe
    )
    if new_recipe:
        return {"message": "updated"}
    else:
        raise HTTPException(status_code=404)


@app.get("/")
async def root():
    return {"message": "Tomato"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
