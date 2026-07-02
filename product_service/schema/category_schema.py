from pydantic import BaseModel
from uuid import UUID
from .product_schema import ProductResponseSchema

class CategoryCreateSchema(BaseModel):
    category_name : str

class CategoryupdateSchema(BaseModel):
    category_name : str
    model_config ={
        'from_attributes':True
    }

class CategoryResponseSchema(BaseModel):
    id : UUID
    category_name : str
    products : list[ProductResponseSchema]
    model_config = {
        'from_attributes':True
    }