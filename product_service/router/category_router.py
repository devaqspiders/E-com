from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.dependencies import get_db
from uuid import UUID, uuid4
from fastapi import APIRouter
from schema.category_schema import CategoryCreateSchema, CategoryResponseSchema
from models.categorymodel import Category
from database.dependencies import get_db

router = APIRouter()

@router.post('/', response_model=CategoryResponseSchema)
def create_category(category: CategoryCreateSchema, db: Session = Depends(get_db)):
    category = Category(id=uuid4(), category_name=category.category_name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.get('/', response_model = list[CategoryResponseSchema])
def get_categories(db : Session = Depends(get_db)):
    category = db.query(Category).all()
    return category