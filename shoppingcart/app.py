import psycopg2
from sqlalchemy import create_engine
from shoppingcart.model.user import User, Base
from shoppingcart.model.product import Product, ProductBase
from shoppingcart.model.order import Order, OrderBase
from shoppingcart.model.cart import Cart, CartBase

is_db_connected = True

db = None
base = None
session = None
try:
    db = create_engine('postgresql://test:123@localhost:5432/shoppingcart')
    from sqlalchemy.orm import sessionmaker
    session = sessionmaker()
    session.configure(bind=db)
    #Base.metadata.drop_all(bind=db)
    Base.metadata.create_all(bind=db)
    ProductBase.metadata.create_all(bind=db)
    CartBase.metadata.create_all(bind=db)
    OrderBase.metadata.create_all(bind=db)
except Exception as err:
    print err
    is_db_connected = False
    print "I am unable to connect to the database"


def login(user_name, password):
    s = session()
    return s.query(User).filter(User.name == user_name, User.password == password).one()

def get_product(product_id):
    print product_id
    s = session()
    return s.query(Product).filter_by(id=product_id).first()

def get_all_products():
    s = session()
    return s.query(Product).filter().all()

def get_cart(user):
    s = session()
    return s.query(Cart).filter_by(user_id=user.id).all()

def get_all_orders():
    s = session()
    return s.query(Order).filter().all()

def get_user_orders(user):
    s = session()
    return s.query(Order).filter_by(user_id = user.id).all()

def get_user(user_id):
    s = session()
    return s.query(User).filter_by(id=user_id).first()

def run():
    if not is_db_connected:
        return False
    
    '''user = User(name="admin", password="admin", fullname="Administrator", role = "admin")  
    s = session()
    s.add(user)  

    user1 = User(name="test", password="test", fullname="Administrator", role = "user")  
    s.add(user1)
    s.commit()'''

    print "----------LOGIN---------"
    user_name = raw_input("USERNAME :")
    password = raw_input("PASSWORD :")

    user = login(user_name, password)
    if user:
        exit = False
        cart_dict = {}
        while (not exit):
            
            if user.role in 'admin':
                input = raw_input('''
                    1. List all produts
                    2. Add/Delete Products
                    3. Orders
                ''')
                input = int(input)
                if input == 1:
                    print "---------------PRODUCTS------------------"
                    for product in get_all_products():
                        print "{} {} {} {} ".format(product.id, product.name, str(product.price), str(product.quantity))
                elif input == 2:
                    product_input = raw_input().split(" ");
                    product = Product(name = product_input[0], price = float(product_input[1]), quantity = int(product_input[2]))
                    s = session()
                    s.add(product)
                    s.commit()

                elif input == 3:
                    print "---------------ORDERS------------------"
                    for order in get_all_orders():
                        user = get_user(order.user_id)
                        product = get_product(order.product_id)
                        print "{} {} {} {}".format(order.id, user.name, product.name, order.total)
                else:
                    print "Exiting............"
                    exit = True
            
            elif user.role in 'user':
                input = raw_input('''
                    1. List all produts
                    2. Add/Delete Cart
                    3. Orders
                ''')

                if int(input) == 1:
                    print "---------------PRODUCTS------------------"
                    for product in get_all_products():
                        print "{} {} {} {} ".format(product.id, product.name, product.price, product.quantity)
                elif int(input) == 2:
                    cart_input = raw_input().split(" ")
                    if int(cart_input[0]) == 1:
                        cart = Cart(user_id = user.id, product_id = cart_input[1], quantity = cart_input[2])

                        print "---------SELECT 1 TO ORDER---------"
                        buy = raw_input()
                        if int(buy) == 1:
                            product = get_product(cart_input[1])
                            total = float(product.price) * int(cart.quantity)
                            
                            total = str(total)
                            order = Order(user_id = user.id, product_id = product.id, total = total)
                            s = session()
                            s.add(order)
                            s.commit()
                         
                elif int(input) == 3:
                    print "---------------ORDERS------------------"
                    print "id user product total"
                    for order in get_user_orders(user):
                        user = get_user(order.user_id)
                        product = get_product(order.product_id)
                        print "{} {} {} {}".format(order.id, user.name, product.name, order.total)
                else:
                    print "Exiting............."
                    exit = True

            else:
                pass
            
        
