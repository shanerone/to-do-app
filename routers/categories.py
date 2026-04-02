from typing import List

from db.database import get_db
from models.categories import CategoriesORM
from schemas.categories import SCategory, SCategoryAdd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, status

router = APIRouter(prefix="/category", tags=["categories"])


def categoryorm_to_model(category_orm: CategoriesORM) -> SCategory:
    return SCategory(id=category_orm.id, title=category_orm.title)


@router.get("/")
async def ger_categories(db: AsyncSession = Depends(get_db)) -> List[SCategory]:
    res = await db.scalars(select(CategoriesORM))
    category_from_bd = res.all()
    return [categoryorm_to_model(category) for category in category_from_bd]


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=SCategory)
async def add_category(
    payload: SCategoryAdd, db: AsyncSession = Depends(get_db)
) -> SCategory:
    category = CategoriesORM(title=payload.title)
    db.add(category)
    await db.commit()
    await db.refresh(category)

    return categoryorm_to_model(category)