from pydantic import BaseModel


class SCategory(BaseModel):
    id: str
    title: str


class SCategoryAdd(BaseModel):
    title: str
    color: str = "#b98b43"


class SCategoryUpdate(BaseModel):
    title: str | None = None
