from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.dependencies import get_db
from uuid import UUID, uuid4
from fastapi import APIRouter
from schema.category_schema import CategoryCreateSchema, CategoryResponseSchema, CategoryupdateSchema
from models.categorymodel import Category
from database.dependencies import get_db
from auth import role

router = APIRouter()

@router.post('/', response_model=CategoryResponseSchema)
def create_category(category: CategoryCreateSchema, db: Session = Depends(get_db), user: dict=Depends(role.required_role('Admin','admin'))):
    category = Category(id=uuid4(), category_name=category.category_name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.get('/', response_model = list[CategoryResponseSchema])
def get_categories(db : Session = Depends(get_db)):
    category = db.query(Category).all()
    return category

@router.get('/{id}', response_model=CategoryResponseSchema)
def get_category(id: UUID, db: Session=Depends(get_db)):
    data = db.query(Category).filter(Category.id==id).first()
    return data

@router.patch('/{id}', response_model=CategoryResponseSchema)
def update_category(id: UUID, db: Session=Depends(get_db), request: dict = CategoryupdateSchema, user: dict=Depends(role.required_role('Admin','admin'))):
    data = db.query(Category).filter(Category.id==id).first()
    data.category_name = request.category_name
    return data