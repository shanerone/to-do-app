from pydantic import BaseModel, EmailStr


class SUser(BaseModel):
    email: EmailStr
    password: str


class SUserLogin(BaseModel):
    email: EmailStr
    password: str


class SUserLogout(BaseModel):
    id: str
    email: str


class SToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
