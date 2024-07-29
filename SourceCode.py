import uuid
import json
import os

# File paths for data storage
USERS_FILE = 'users.json'
ADMINS_FILE = 'admins.json'
PRODUCTS_FILE = 'products.json'
CATEGORIES_FILE = 'categories.json'
CARTS_FILE = 'carts.json'

# Load data from JSON files
def load_json(file_path, default_value=None):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return default_value if default_value is not None else {}

# Save data to JSON files
def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Initialize data files with default values if they don't exist
def initialize_data():
    if not os.path.exists(USERS_FILE):
        save_json(USERS_FILE, {})
    if not os.path.exists(ADMINS_FILE):
        save_json(ADMINS_FILE, {'admin': 'admin123'})
    if not os.path.exists(PRODUCTS_FILE):
        save_json(PRODUCTS_FILE, [])
    if not os.path.exists(CATEGORIES_FILE):
        save_json(CATEGORIES_FILE, {'1': 'Footwear', '2': 'Clothing', '3': 'Electronics'})
    if not os.path.exists(CARTS_FILE):
        save_json(CARTS_FILE, {})

initialize_data()

# Load data
users_db = load_json(USERS_FILE)
admins_db = load_json(ADMINS_FILE)
products_db = load_json(PRODUCTS_FILE)
categories_db = load_json(CATEGORIES_FILE)
carts = load_json(CARTS_FILE)

# Utility Functions
def generate_session_id():
    return str(uuid.uuid4())

def find_product_by_id(product_id):
    for product in products_db:
        if product['id'] == product_id:
            return product
    return None

def find_category_by_id(category_id):
    return categories_db.get(category_id, None)

# Classes
class User:
    def _init_(self, username, password):
        self.username = username
        self.password = password
        self.session_id = None

    def login(self, password):
        if self.password == password:
            self.session_id = generate_session_id()
            print(f"Welcome {self.username}! Your session ID is {self.session_id}.")
            return True
        else:
            print("Invalid password!")
            return False

    def view_cart(self):
        if self.session_id in carts and carts[self.session_id]:
            total_price = 0
            print(f"Cart for {self.username}:")
            for item in carts[self.session_id]:
                product = find_product_by_id(item['product_id'])
                if product:
                    product_name = product['name']
                    product_price = product['price']
                    quantity = item['quantity']
                    item_total = product_price * quantity
                    total_price += item_total
                    print(f" - {product_name} (Quantity: {quantity}, Price: {product_price}, Total: {item_total})")
            print(f"Total price: {total_price}")
        else:
            print("No items in your cart!")

    def view_products(self):
        if products_db:
            print("Available Products:")
            for product in products_db:
                print(f"ID: {product['id']}, Name: {product['name']}, Category: {find_category_by_id(product['category_id'])}, Price: {product['price']}")
        else:
            print("No products available!")

    def add_to_cart(self, product_id, quantity):
        product = find_product_by_id(product_id)
        if not product:
            print("Product not found!")
            return
        if self.session_id not in carts:
            carts[self.session_id] = []
        carts[self.session_id].append({'product_id': product_id, 'quantity': quantity})
        save_json(CARTS_FILE, carts)
        print(f"Added {quantity} of {product['name']} to your cart.")

    def remove_from_cart(self, product_id):
        if self.session_id in carts:
            cart_items = carts[self.session_id]
            carts[self.session_id] = [item for item in cart_items if item['product_id'] != product_id]
            save_json(CARTS_FILE, carts)
            print(f"Removed product ID {product_id} from your cart.")
        else:
            print("Cart is empty!")

    def checkout(self, payment_option):
        if self.session_id in carts and carts[self.session_id]:
            print(f"Processing payment with {payment_option}. Your order is successfully placed!")
            carts[self.session_id] = []
            save_json(CARTS_FILE, carts)
        else:
            print("Your cart is empty!")

class Admin:
    def _init_(self, username, password):
        self.username = username
        self.password = password
        self.session_id = None

    def login(self, password):
        if self.password == password:
            self.session_id = generate_session_id()
            print(f"Welcome Admin {self.username}! Your session ID is {self.session_id}.")
            return True
        else:
            print("Invalid password!")
            return False

    def add_product(self, product_id, name, category_id, price):
        if find_category_by_id(category_id):
            products_db.append({'id': product_id, 'name': name, 'category_id': category_id, 'price': price})
            save_json(PRODUCTS_FILE, products_db)
            print(f"Product {name} added successfully.")
        else:
            print("Invalid category ID!")

    def update_product(self, product_id, name=None, category_id=None, price=None):
        product = find_product_by_id(product_id)
        if product:
            if name:
                product['name'] = name
            if category_id and find_category_by_id(category_id):
                product['category_id'] = category_id
            if price:
                product['price'] = price
            save_json(PRODUCTS_FILE, products_db)
            print(f"Product ID {product_id} updated successfully.")
        else:
            print("Product not found!")

    def remove_product(self, product_id):
        global products_db
        products_db = [product for product in products_db if product['id'] != product_id]
        save_json(PRODUCTS_FILE, products_db)
        print(f"Product ID {product_id} removed successfully.")

    def add_category(self, category_id, category_name):
        categories_db[category_id] = category_name
        save_json(CATEGORIES_FILE, categories_db)
        print(f"Category {category_name} added successfully.")

    def remove_category(self, category_id):
        if category_id in categories_db:
            del categories_db[category_id]
            save_json(CATEGORIES_FILE, categories_db)
            print(f"Category ID {category_id} removed successfully.")
        else:
            print("Category not found!")

# Main Functions
def user_interface():
    print("Welcome to the Demo Marketplace")
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    if username in users_db:
        user = User(username, users_db[username])
    else:
        user = User(username, password)
        users_db[username] = password
        save_json(USERS_FILE, users_db)
    
    if user.login(password):
        while True:
            print("\n1) View Products")
            print("2) View Cart")
            print("3) Add to Cart")
            print("4) Remove from Cart")
            print("5) Checkout")
            print("6) Logout")
            choice = input("Choose an action: ")
            if choice == '1':
                user.view_products()
            elif choice == '2':
                user.view_cart()
            elif choice == '3':
                product_id = input("Enter product ID to add: ")
                quantity = int(input("Enter quantity: "))
                user.add_to_cart(product_id, quantity)
            elif choice == '4':
                product_id = input("Enter product ID to remove: ")
                user.remove_from_cart(product_id)
            elif choice == '5':
                payment_option = input("Choose payment option (Net banking/PayPal/UPI): ")
                user.checkout(payment_option)
            elif choice == '6':
                print("Logged out.")
                break
            else:
                print("Invalid choice!")

def admin_interface():
    print("Welcome to the Admin Dashboard")
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    
    if username in admins_db and admins_db[username] == password:
        admin = Admin(username, password)
        if admin.login(password):
            while True:
                print("\n1) Add Product")
                print("2) Update Product")
                print("3) Remove Product")
                print("4) Add Category")
                print("5) Remove Category")
                print("6) Logout")
                choice = input("Choose an action: ")
                if choice == '1':
                    product_id = input("Enter product ID: ")
                    name = input("Enter product name: ")
                    category_id = input("Enter category ID: ")
                    price = float(input("Enter product price: "))
                    admin.add_product(product_id, name, category_id, price)
                elif choice == '2':
                    product_id = input("Enter product ID to update: ")
                    name = input("Enter new product name (or leave blank): ")
                    category_id = input("Enter new category ID (or leave blank): ")
                    price = input("Enter new price (or leave blank): ")
                    price = float(price) if price else None
                    admin.update_product(product_id, name, category_id, price)
                elif choice == '3':
                    product_id = input("Enter product ID to remove: ")
                    admin.remove_product(product_id)
                elif choice == '4':
                    category_id = input("Enter new category ID: ")
                    category_name = input("Enter new category name: ")
                    admin.add_category(category_id, category_name)
                elif choice == '5':
                    category_id = input("Enter category ID to remove: ")
                    admin.remove_category(category_id)
                elif choice == '6':
                    print("Logged out.")
                    break
                else:
                    print("Invalid choice!")
    else:
        print("Invalid admin credentials!")

def main():
    print("Welcome to the Demo Marketplace")
    role = input("Are you a User or Admin? (U/A): ").strip().upper()
    
    if role == 'U':
        user_interface()
    elif role == 'A':
        admin_interface()
    else:
        print("Invalid role selected!")

if _name_ == "_main_":
    main()
