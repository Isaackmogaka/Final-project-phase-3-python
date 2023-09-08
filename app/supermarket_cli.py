# Import necessary modules and classes from SQLAlchemy and your models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Category, Product, Customer, Order, OrderDetail

# Create a SQLAlchemy engine and session, connecting to a SQLite database named 'supermarket.db'
engine = create_engine('sqlite:///supermarket.db')
Session = sessionmaker(bind=engine)
session = Session()

# Function to add a new item (Product, Category, or Customer)
def add_item(model, item_name, item_price=None):
    print(f"Adding a New {item_name.capitalize()}:")
    entered_name = input(f"Enter {item_name} name: ")

    # Create a new item object with user input
    if model == Product:
        item_price = float(input(f"Enter {item_name} price: "))  # Prompt for the price as a float
    item = model(**{f"{item_name.lower()}_name": entered_name, "price": item_price} if model == Product else {f"{item_name.lower()}_name": entered_name})
    
    session.add(item)
    session.commit()
    print(f"{entered_name.capitalize()} added successfully!")

# Function to place a new order
def place_order():
    print("Placing a New Order:")

    # Get the customer's name from the user
    customer_name = input("Enter customer name: ").strip()
    customer = session.query(Customer).filter_by(customer_name=customer_name).first()

    if not customer:
        print("Customer not found.")
        return

    # Create a new order for the customer
    order = Order(customer_id=customer.customer_id)
    session.add(order)
    session.commit()

    # Allow the user to add products to the order
    while True:
        product_name = input("Enter product name (or 'done' to finish): ").strip()

        if product_name.lower() == 'done':
            break

        product = session.query(Product).filter_by(product_name=product_name).first()

        if not product:
            print(f"Product '{product_name}' not found.")
            continue

        quantity = int(input(f"Enter quantity for '{product_name}': ").strip())

        # Create an order detail for the product in the order
        order_detail = OrderDetail(order_id=order.order_id, product_id=product.product_id, quantity=quantity)
        session.add(order_detail)
        session.commit()

    print("Order placed successfully!")

# Function to view order details
def order_details():
    print("View Order Details:")

    # Get the order ID or customer name from the user
    order_id_or_customer_name = input("Enter order ID or customer name: ").strip()

    # Check if the input is an order ID (numeric)
    if order_id_or_customer_name.isdigit():
        order_id = int(order_id_or_customer_name)
        order = session.query(Order).filter_by(order_id=order_id).first()

        if not order:
            print(f"Order with ID {order_id} not found.")
            return

        # Display order details including products and quantities
        print(f"Order ID: {order.order_id}, Customer: {order.customer.customer_name}")
        print("Order Details:")
        for detail in order.order_details:
            print(f"Product: {detail.product.product_name}, Quantity: {detail.quantity}")

    # Check if the input is a customer name
    else:
        customer = session.query(Customer).filter_by(customer_name=order_id_or_customer_name).first()

        if not customer:
            print(f"Customer '{order_id_or_customer_name}' not found.")
            return

        # Display customer's orders including order IDs and dates
        print(f"Customer: {customer.customer_name}")
        print("Orders:")
        for order in customer.orders:
            print(f"Order ID: {order.order_id}, Date: {order.order_date}")

    # Handle the case if the input is neither a valid order ID nor a customer name
    print("Invalid input. Please enter a valid order ID or customer name.")

# Main menu for user interaction
def main_menu():
    print("Welcome to the Supermarket CLI Application!")
    while True:
        print("\nAvailable Commands:")
        print("add_product: Add a new product")
        print("add_category: Add a new category")
        print("add_customer: Add a new customer")
        print("place_order: Place a new order")
        print("order_details: View order details")
        print("exit: Exit the application")

        user_input = input("Enter a command: ").strip().lower()

        if user_input == "exit":
            break

        # Call the appropriate function based on user input
        if user_input == "add_product":
            add_item(Product, "product")
        elif user_input == "add_category":
            add_item(Category, "category")
        elif user_input == "add_customer":
            add_item(Customer, "customer")
        elif user_input == "place_order":
            place_order()
        elif user_input == "order_details":
            order_details()
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main_menu()  # Start the main menu loop when the script is executed




