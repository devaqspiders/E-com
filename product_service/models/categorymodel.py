from database.connection import Base
from sqlalchemy import Column, String, Integer, Float, UUID
from sqlalchemy.orm import relationship

class Category(Base):
    __tablename__ = 'category'
    id =  Column(UUID, primary_key=True, unique=True)
    category_name = Column(String(150))
    products = relationship('Product', back_populates='category')