from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Model


class CategoriesORM(Model):
    __tablename__ = "categories"

    title: Mapped[str] = mapped_column(String(25), nullable=False)
