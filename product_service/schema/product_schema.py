from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal
# from .category_schema import CategoryResponseSchema
from .productimg_schema import ProductImgResponse

class ProductResponseSchema(BaseModel):
    id : UUID
    name : str
    desc : str | None = None
    price : Decimal
    images_rel : list[ProductImgResponse]
    category_id : UUID
    # category : CategoryResponseSchema
    model_config = {
        'from_attributes' : True
    }

class ProductResponsePagination(BaseModel):
    item: list[ProductResponseSchema]
    page: int 
    limit: int 
    total: int
    total_pages: int
    has_next: bool
    has_previous: bool


class ProductModifySchema(BaseModel):
    name : str | None = None
    desc : str | None = None
    price : Decimal | None = None
    image : str | None = None
    category_id : UUID | None = None

    model_config = {
        'from_attributes' : True
    }