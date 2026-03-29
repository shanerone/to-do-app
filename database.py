from uuid import uuid4
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:15432/postgres"
engine = create_async_engine(DATABASE_URL)

new_session = async_sessionmaker(engine)


class Model(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, default=lambda: str(uuid4()))

class TaskORM(Model):
    __tablename__ = "tasks"
    
    