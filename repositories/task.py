from typing import List, Optional

from models.task import TaskORM
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class TaskRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all(self) -> List[TaskORM]:
        result = await self.db.scalars(select(TaskORM))
        return result.all()

    async def get_by_id(self, id: str) -> Optional[TaskORM]:
        return await self.db.get(TaskORM, id)

    async def add(self, task: TaskORM) -> TaskORM:
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def update(self, task: TaskORM) -> TaskORM:
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete(self, task: TaskORM) -> None:
        await self.db.delete(task)
        await self.db.commit()
