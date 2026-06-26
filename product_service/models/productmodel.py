from sqlalchemy import Column, String, UUID, Text, Numeric, ForeignKey, TIMESTAMP, func
from database.connection import Base
from sqlalchemy.orm import relationship
from uuid import uuid4

class Product(Base):
    __tablename__ = 'product'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(200), nullable=False)
    desc = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    category_id = Column(UUID(as_uuid=True),ForeignKey('category.id'), nullable=False)
    created_at = Column(TIMESTAMP(True),server_default=func.now())
    category = relationship('Category', back_populates='products')
    images_rel = relationship('ProductImage', back_populates='product_rel')