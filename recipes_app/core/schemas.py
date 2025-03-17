from pydantic import BaseModel, ConfigDict


class BaseRecipe(BaseModel):
    title: str
    cooking_time: int


class RecipeCreate(BaseRecipe):
    text: str
    ingredients_list: str
    pass


class RecipeReadAll(BaseRecipe):
    id: int
    number_view: int
    pass

    class Config:
        orm_mode = True


class RecipeRead(BaseRecipe):
    text: str
    ingredients_list: str
    number_view: int

    class Config:
        orm_mode = True


class RecipeUpdate(BaseRecipe):
    title: str | None = None
    cooking_time: int | None = None
    text: str | None = None


class Recipe(BaseRecipe):
    model_config = ConfigDict(from_attributes=True)
