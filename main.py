from uuid import uuid4

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from fastapi import FastAPI

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=["http://localhost:3000"], allow_methods=["*"]
)


class STasks(BaseModel):
    id: str
    title: str
    completed: bool


class STaskAdd(BaseModel):
    title: str


class STaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None


tasks: list[STasks] = []


@app.get("/tasks")
async def get_tasks() -> list[STasks]:
    return tasks


@app.post("/tasks")
async def add_task(payload: STaskAdd) -> STasks:
    task = STasks(id=str(uuid4()), title=payload.title, completed=False)

    tasks.append(task)
    return task


@app.patch("/tasks/{task_id}")
async def update_task(task_id: str, payload: STaskUpdate):
    for task in tasks:
        if task.id == task_id:
            task.title = payload.title if payload.title else task.title
            task.completed = (
                payload.completed if payload.completed is not None else task.completed
            )

            return task


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
