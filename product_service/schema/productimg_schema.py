from pydantic import BaseModel
from uuid import UUID

class ProductImgResponse(BaseModel):
    id : UUID
    image : str