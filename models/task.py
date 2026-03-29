from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Model


class TaskORM(Model):
    __tablename__ = "tasks"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    completed: Mapped[bool] = mapped_column(default=False)
