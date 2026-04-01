from contextlib import asynccontextmanager
from typing import List

from db.database import create_tables, get_db, delete_tables
from fastapi.middleware.cors import CORSMiddleware
from models.categories import CategoriesORM
from models.task import TaskORM
from schemas.categories import SCategory, SCategoryAdd, SCategoryUpdate
from schemas.task import STaskAdd, STasks, STaskUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends, FastAPI, HTTPException, status


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await delete_tables()
    await create_tables()
    print("DB ready")
    yield
    print("Off")


app = FastAPI(title="To-Do App", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware, allow_origins=["http://localhost:3000"], allow_methods=["*"]
)


def taskorm_to_model(task_orm: TaskORM) -> STasks:
    return STasks(id=task_orm.id, title=task_orm.title, completed=task_orm.completed)


def categoryorm_to_model(category_orm: CategoriesORM) -> SCategory:
    return SCategory(id=category_orm.id, title=category_orm.title)


@app.get("/tasks", response_model=List[STasks])
async def get_tasks(db: AsyncSession = Depends(get_db)) -> List[STasks]:
    result = await db.scalars(select(TaskORM))
    tasks_from_db = result.all()
    return [taskorm_to_model(task) for task in tasks_from_db]


@app.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=STasks)
async def add_task(payload: STaskAdd, db: AsyncSession = Depends(get_db)) -> STasks:
    task = TaskORM(title=payload.title, completed=False)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return taskorm_to_model(task)


@app.patch("/tasks/{task_id}", response_model=STasks)
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


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str, db: AsyncSession = Depends(get_db)):
    task = await db.get(TaskORM, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.delete(task)
    await db.commit()
    return None


@app.get("/categories")
async def ger_categories(db: AsyncSession = Depends(get_db)) -> List[SCategory]:
    res = await db.scalars(select(CategoriesORM))
    category_from_bd = res.all()
    return [categoryorm_to_model(category) for category in category_from_bd]


@app.post("/categories", status_code=status.HTTP_201_CREATED, response_model=SCategory)
async def add_category(
    payload: SCategoryAdd, db: AsyncSession = Depends(get_db)
) -> SCategory:
    category = CategoriesORM(title=payload.title)
    db.add(category)
    await db.commit()
    await db.refresh(category)

    return categoryorm_to_model(category)
    

