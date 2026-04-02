from fastapi.security import OAuth2PasswordRequestForm
from auth.dependencies import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)
from db.database import get_db
from models.user import UserORM
from schemas.user import SToken, SUserLogin, SUserLogout, SUser
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model = SUserLogout, status_code=status.HTTP_201_CREATED)
async def register(payload: SUser, db: AsyncSession = Depends(get_db)):
    existing = await db.scalar(select(UserORM).where(UserORM.email == payload.email))
    if existing:
        raise HTTPException(status_code=400, detail="Email уже занят!")
        
    user = UserORM(email=payload.email, hashed_password = hash_password(payload.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return SUserLogout(id=user.id, email=user.email)
    
@router.post("/login", response_model=SToken)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await db.scalar(select(UserORM).where(UserORM.email == form_data.username))
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный email или пароль")
    token = create_access_token({"sub": user.id})
    
    return SToken(access_token=token)    
    
@router.get("/me", response_model=SUserLogout)
async def get_me(current_user: UserORM = Depends(get_current_user)):
    return SUserLogout(id=current_user.id, email=current_user.email)