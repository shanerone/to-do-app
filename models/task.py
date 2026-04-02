from typing import Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Model


class TaskORM(Model):
    __tablename__ = "tasks"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    completed: Mapped[bool] = mapped_column(default=False)
    category_id: Mapped[Optional[str]] = mapped_column(
            String(36), ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
        )