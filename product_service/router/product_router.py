from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, Query
from schema.product_schema import ProductModifySchema, ProductResponseSchema
from sqlalchemy.orm import Session
from database.dependencies import get_db
from models.productmodel import Product
from models.categorymodel import Category
from models.productimgmodel import ProductImage
from uuid import UUID, uuid4
from decimal import Decimal
from auth import role, security
from sqlalchemy import or_

router = APIRouter()

@router.get('',response_model= list[ProductResponseSchema])
def get_products(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=20),
    search: str | None = None,
    category_id: UUID | None = None,
    min_price: Decimal | None = None,
    max_price: Decimal | None = None,
    sort: str | None = None,
    db: Session = Depends(get_db)):
    products = db.query(Product)
    if search:
        query = query.filter(
        or_(
            Product.name.ilike(f"%{search}%"),
            Product.description.ilike(f"%{search}%"),
            Product.brand.ilike(f"%{search}%")
        )
        )
    if category_id:
        query = query.filter(Product.category_id == category_id)

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if sort == "price_asc":
        query = query.order_by(Product.price.asc())

    elif sort == "price_desc":
        query = query.order_by(Product.price.desc())

    elif sort == "newest":
        query = query.order_by(Product.created_at.desc())
    offset = (page-1)*limit
    products = query.offset(offset).limit(limit).all()
    return products

@router.get('/{product_id}', response_model=ProductResponseSchema)
def get_product(product_id: UUID, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    return product

@router.post('', response_model=ProductResponseSchema)
async def create_product(name : str = Form(...), desc : str = Form(...), price : Decimal = Form(...), images : list[UploadFile] = Form(...), category_name : str = Form(...), db: Session = Depends(get_db), user: dict=Depends(role.required_role('Admin','admin'))):
    category = db.query(Category).filter(Category.category_name == category_name).first()

    product = Product(
            id = uuid4(),
            name = name, 
            desc = desc, 
            price = price, 
            category_id = category.id,
        )
    db.add(product)
    db.flush()

    for image in images:
        extension = image.filename.rsplit(".", 1)[1]
        file_path = f'media/{uuid4()}.{extension}'
        with open(file_path, 'wb') as buffer:
            buffer.write(await image.read())
        product_img = ProductImage(
            image=file_path,
            product_id=product.id
        )
        db.add(product_img)
    db.commit()
    db.refresh(product)
    return product

@router.put('/{product_id}', response_model= ProductResponseSchema)
def update_product(product_id: UUID, data: ProductModifySchema, db: Session = Depends(get_db), user: dict=Depends(role.required_role('Admin','admin'))):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return HTTPException(status_code= 404, detail= 'product not found')
    

@router.patch('/{product_id}', response_model= ProductResponseSchema)
def modify_product(product_id: UUID, data: ProductModifySchema, db: Session = Depends(get_db), user: dict=Depends(role.required_role('Admin','admin'))):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return HTTPException(status_code=404, detail="product not found")
    
    updated_data = data.model_dump(exclude_unset=True)

    for key, value in updated_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return product

@router.delete('/{product_id}')
def remove_product(product_id: UUID, db: Session=Depends(get_db), user: dict=Depends(role.required_role('seller','Seller','Admin','admin'))):
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return HTTPException(status_code=404, detail="product not found")
        db.delete(product)
        db.commit()
        return {'message' : 'deleted successfull'}
