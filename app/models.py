# Import necessary modules and classes from SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Create a SQLAlchemy engine and sesssion
engine = create_engine('sqlite:///supermarket.db')
Session = sessionmaker(bind=engine)
session = Session()

# Create a SQLAlchemy base
Base = declarative_base()

# Define the Categories table
class Category(Base):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True)
    category_name = Column(String)
      # Define the relationship with products
    products = relationship('Product', back_populates='category')

# Define the Products table
class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String, nullable=False)
    price = Column(Float,nullable=False)
    category_id = Column(Integer, ForeignKey('categories.category_id'))

    
    category = relationship('Category', back_populates='products')
    orders = relationship('OrderDetail', back_populates='product',overlaps="orders")
    order_details = relationship('OrderDetail', back_populates='product',overlaps="orders")
  
# Establish a relationship with categories
    category = relationship('Category', back_populates='products')
    order_details = relationship('OrderDetail', back_populates='product',overlaps="orders")
    orders = relationship('Order', back_populates='customer')
    orders = relationship('OrderDetail', back_populates='product')
# Define the Customers table
class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True)
    customer_name = Column(String)
    orders = relationship('Order', back_populates='customer')

# Define the Orders table
class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True)
    order_date = Column(Date)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))

    # Establish a relationship with order details
    customer = relationship('Customer', back_populates='orders')
    order_details = relationship('OrderDetail', back_populates='order')

# Define the OrderDetails table
class OrderDetail(Base):
    __tablename__ = 'order_details'

    order_detail_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'))
    product_id = Column(Integer, ForeignKey('products.product_id'))
    quantity = Column(Integer)

    # Establish relationships with order and product
    order = relationship('Order', back_populates='order_details')
    product = relationship('Product', back_populates='order_details',overlaps="orders")

# Create the tables in the database using the base metadata
Base.metadata.create_all(engine)