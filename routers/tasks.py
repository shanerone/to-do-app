from typing import List

from auth.dependencies import get_current_user
from db.database import get_db
from models.task import TaskORM
from models.user import UserORM
from schemas.task import STaskAdd, STasks, STaskUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/tasks", tags=["tasks"])


def taskorm_to_model(task_orm: TaskORM) -> STasks:
    return STasks(id=task_orm.id, title=task_orm.title, completed=task_orm.completed)


@router.get("/", response_model=List[STasks])
async def get_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: UserORM = Depends(get_current_user),
) -> List[STasks]:
    result = await db.scalars(select(TaskORM))
    tasks_from_db = result.all()
    return [taskorm_to_model(task) for task in tasks_from_db]


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=STasks)
async def add_task(payload: STaskAdd, db: AsyncSession = Depends(get_db)) -> STasks:
    task = TaskORM(title=payload.title, completed=False)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return taskorm_to_model(task)


@router.patch("/{task_id}", response_model=STasks)
async def update_task(
    task_id: str, payload: STaskUpdate, db: AsyncSession = Depends(get_db)
) -> STasks:
    task = await db.get(TaskORM, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if payload.title is not None:
        task.title = payload.title
    if payload.completed is not None:
        task.completed = payload.completed

    await db.commit()
    await db.refresh(task)

    return taskorm_to_model(task)
    

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str, db: AsyncSession = Depends(get_db)):
    task = await db.get(TaskORM, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.delete(task)
    await db.commit()
    return None