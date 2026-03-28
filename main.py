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


tasks: list[STasks] = []


@app.get("/tasks")
async def get_tasks() -> list[STasks]:
    return tasks


@app.post("/tasks")
async def add_task(payload: STaskAdd) -> STasks:
    task = STasks(id=str(uuid4()), title=payload.title, completed=False)

    tasks.append(task)
    return task
