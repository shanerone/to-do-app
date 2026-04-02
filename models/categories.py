from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Model


class CategoriesORM(Model):
    __tablename__ = "categories"

    title: Mapped[str] = mapped_column(String(25), nullable=False)
    color: Mapped[str] = mapped_column(String(7), default="#b98b43")