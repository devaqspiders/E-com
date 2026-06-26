from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, Query
from schema.product_schema import ProductModifySchema, ProductResponseSchema
from sqlalchemy.orm import Session
from database.dependencies import get_db
from models.productmodel import Product
from models.categorymodel import Category
from models.productimgmodel import ProductImage
from uuid import UUID, uuid4
from decimal import Decimal

router = APIRouter()

@router.get('/',response_model= list[ProductResponseSchema])
def get_products(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=20),
    db: Session = Depends(get_db)):
    offset = (page-1)*limit
    products = db.query(Product).offset(offset).limit(limit).all()
    return products

@router.get('/{product_id}', response_model=ProductResponseSchema)
def get_product(product_id: UUID, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    return product

@router.post('/')
async def create_product(name : str = Form(...), desc : str = Form(...), price : Decimal = Form(...), images : list[UploadFile] = Form(...), category_name : str = Form(...), db: Session = Depends(get_db)):
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
    return {'name':name, 'desc':desc, 'price':price, 'images':images, 'category':category_name}

@router.put('/{product_id}', response_model= ProductResponseSchema)
def update_product(product_id: UUID, data: ProductModifySchema, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return HTTPException(status_code= 404, detail= 'product not found')
    

@router.patch('/{product_id}', response_model= ProductResponseSchema)
def modify_product(product_id: UUID, data: ProductModifySchema, db: Session = Depends(get_db)):
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
def remove_product(product_id: UUID, db: Session=Depends(get_db)):
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return HTTPException(status_code=404, detail="product not found")
        db.delete(product)
        db.commit()
        return {'message' : 'deleted successfull'}
