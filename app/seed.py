# Import necessary modules and classes from SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Category, Product, Customer, Order, OrderDetail

# Create a SQLAlchemy engine and session, connecting to a SQLite database named 'supermarket.db'
engine = create_engine('sqlite:///supermarket.db')
Session = sessionmaker(bind=engine)
session = Session()

# Create the database tables based on the models defined in 'models.py'
Base.metadata.create_all(engine)

# Create instances of your model classes (empty instances)
category1 = Category()
category2 = Category()

product1 = Product()
product2 = Product()

customer1 = Customer()
customer2 = Customer()

order1 = Order()
order2 = Order()

order_detail1 = OrderDetail()
order_detail2 = OrderDetail()

# Add the instances to the session (staging them for database insertion)
session.add_all([category1, category2, product1, product2, customer1, customer2, order1, order2, order_detail1, order_detail2])

# Commit the changes to the database (persisting the instances to the database)
session.commit()

# Close the session (releasing resources)
session.close()
