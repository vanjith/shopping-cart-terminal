from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

ProductBase = declarative_base()

class Product(ProductBase):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(String)
    quantity = Column(Integer)