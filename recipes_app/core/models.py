from sqlalchemy.orm import Mapped, mapped_column
from ..CRUD.database import Base


class Recipe(Base):
    __tablename__: str = "Recipe"
    __table_args__ = {"extend_existing": True}
    title: Mapped[str]
    number_view: Mapped[int] = mapped_column(default=0)
    cooking_time: Mapped[int]
    text: Mapped[str]
    ingredients_list: Mapped[str]
