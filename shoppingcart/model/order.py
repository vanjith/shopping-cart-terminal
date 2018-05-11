from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from shoppingcart.model.user import User
from shoppingcart.model.product import Product

OrderBase = declarative_base()

class Order(OrderBase):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey(User.id))
    product_id = Column(ForeignKey(Product.id))
    total = Column(String)
