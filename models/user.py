from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Model


class UserORM(Model):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
