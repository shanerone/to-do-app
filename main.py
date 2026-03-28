from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

tasks = []

class STask(BaseModel):
    id:str
    title:str
    completed:bool

@app.get("/tasks")
def get_tasks():
    return tasks