from sqlalchemy.future import select
from typing import Sequence
from .database import AsyncSession
from core import schemas
from core.models import Recipe
from sqlalchemy import desc


async def get_all_recipes(
        session: AsyncSession,
) -> Sequence[Recipe]:
    res = await session.execute(select(Recipe).
                                order_by(desc(Recipe.number_view), Recipe.cooking_time))
    return res.scalars().all()


async def creat_new_recipe(session: AsyncSession,
                           recipe_create: schemas.RecipeCreate,
                           ) -> Recipe:
    recipe = Recipe(**recipe_create.dict())
    session.add(recipe)
    await session.commit()
    return recipe


async def get_id_recipe(session: AsyncSession,
                        recipe_id: int,
                        ) -> Recipe:
    # await session.execute(select(Recipe)).all()
    return await session.get(Recipe, recipe_id)


async def update_product(
        session: AsyncSession,
        recipe_update: schemas.RecipeUpdate,
        partial: bool = False,
) -> Recipe:
    for name, value in recipe_update.model_dump(exclude_unset=partial).items():
        setattr(Recipe, name, value)
    await session.commit()
    # return product


async def update_number_view(
        session: AsyncSession,
        recipe: Recipe):
    recipe.number_view = int(recipe.number_view) + 1
    await session.commit()
    return recipe
