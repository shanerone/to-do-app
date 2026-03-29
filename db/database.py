import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Read DATABASE_URL from environment with a sensible default for local dev.
# This avoids hard dependency on a missing `core.config` module and makes the module loadable.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:admin@127.0.0.1:15432/postgres",
)

engine = create_async_engine(DATABASE_URL, echo=False)

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        yield session


async def create_tables():
    # import Model dynamically to avoid circular imports at module import time
    from models.base import Model

    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    from models.base import Model

    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
