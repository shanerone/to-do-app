from pydantic import BaseModel


class STasks(BaseModel):
    id: str
    title: str
    completed: bool


class STaskAdd(BaseModel):
    title: str


class STaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None
