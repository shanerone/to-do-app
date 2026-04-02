from pydantic import BaseModel


class STasks(BaseModel):
    id: str
    title: str
    completed: bool
    category_id: str | None = None


class STaskAdd(BaseModel):
    title: str
    category_id: str | None = None


class STaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None
    category_id: str | None = None
