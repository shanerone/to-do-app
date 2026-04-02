from typing import List

from db.database import get_db
from models.categories import CategoriesORM
from schemas.categories import SCategory, SCategoryAdd, SCategoryUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/categories", tags=["categories"])


def categoryorm_to_model(category_orm: CategoriesORM) -> SCategory:
    return SCategory(id=category_orm.id, title=category_orm.title)


@router.get("")
async def ger_categories(db: AsyncSession = Depends(get_db)) -> List[SCategory]:
    res = await db.scalars(select(CategoriesORM))
    category_from_bd = res.all()
    return [categoryorm_to_model(category) for category in category_from_bd]


@router.post("", status_code=status.HTTP_201_CREATED, response_model=SCategory)
async def add_category(
    payload: SCategoryAdd, db: AsyncSession = Depends(get_db)
) -> SCategory:
    category = CategoriesORM(title=payload.title)
    db.add(category)
    await db.commit()
    await db.refresh(category)

    return categoryorm_to_model(category)
    
@router.patch("/{category_id}")
async def update_category(category_id: str, payload: SCategoryUpdate, db: AsyncSession = Depends(get_db)) -> SCategory:
    category = await db.get(CategoriesORM, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="category not found")
        
    if payload.title is not None:
        category.title = payload.title
    
    await db.commit()
    await db.refresh(category)
    
    return categoryorm_to_model(category)
    
@router.delete("/{category_id}")
async def delete_category(category_id: str, db: AsyncSession = Depends(get_db)):
    category = await db.get(CategoriesORM, category_id)
    
    if not category:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.delete(category)
    await db.commit()
    return None