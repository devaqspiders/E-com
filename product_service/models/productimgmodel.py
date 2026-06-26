from sqlalchemy import Column, String, UUID, Text, Numeric, ForeignKey, TIMESTAMP, func
from database.connection import Base
from sqlalchemy.orm import relationship
from uuid import uuid4

class ProductImage(Base):
    __tablename__ = 'productimage'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    image = Column(String(200), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    product_rel = relationship('Product', back_populates='images_rel')