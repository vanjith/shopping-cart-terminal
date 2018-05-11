from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from shoppingcart.model.user import User
from shoppingcart.model.product import Product

CartBase = declarative_base()

class Cart(CartBase):
    __tablename__ = 'cart'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey(User.id))
    product_id = Column(ForeignKey(Product.id))
    quantity = Column(Integer)
