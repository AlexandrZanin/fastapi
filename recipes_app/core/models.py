from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from CRUD.database import Base


class Recipe(Base):
    __tablename__ = 'Recipe'
    title: Mapped[str]
    number_view: Mapped[int] = mapped_column(default=0)
    cooking_time: Mapped[int]
    text: Mapped[str]
    ingredients_list: Mapped[str]

