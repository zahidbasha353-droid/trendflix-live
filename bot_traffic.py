import os
import django
import random
from faker import Faker  # Fake data generator (Optional, but we use lists here for simplicity)

# 1. SETUP DJANGO ENVIRONMENT
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trendflix_core.settings')
django.setup()

from django.contrib.auth.models import User
from store.models import Product, Order, OrderItem

# 2. FAKE DATA LISTS
first_names = ["Rahul", "Priya", "Ahmed", "Anita", "Suresh", "Divya", "Karthik", "Meera", "Vikram", "Sneha"]
last_names = ["Kumar", "Sharma", "Khan", "Reddy", "Nair", "Patel", "Singh", "Das", "Rao", "Basha"]
cities = ["Chennai", "Mumbai", "Bangalore", "Delhi", "Hyderabad", "Coimbatore", "Madurai"]

print("-" * 40)
print("🤖 TRAFFIC BOT STARTED: Simulating Customers & Orders...")
print("-" * 40)

# 3. GET ALL PRODUCTS
products = list(Product.objects.all())

if not products:
    print("❌ Error: No products found! Run 'bot_inventory.py' first.")
    exit()

# 4. SIMULATE 5 ORDERS
for i in range(1, 6): # Change 6 to higher number for more orders
    # A. Generate Fake Customer
    fname = random.choice(first_names)
    lname = random.choice(last_names)
    username = f"{fname.lower()}{random.randint(100,999)}"
    email = f"{username}@example.com"
    full_name = f"{fname} {lname}"
    
    # Create User Account (if not exists)
    user, created = User.objects.get_or_create(username=username, email=email)
    if created:
        user.set_password("password123")
        user.save()

    print(f"👤 Customer '{full_name}' entered the store...")

    # B. Select Random Products
    num_items = random.randint(1, 3) # Buy 1 to 3 items
    selected_products = random.sample(products, num_items)
    
    total_bill = 0
    order_items = []

    # C. Calculate Bill
    for product in selected_products:
        qty = random.randint(1, 2)
        total_bill += (product.selling_price * qty)
        order_items.append({'product': product, 'qty': qty, 'price': product.selling_price})

    # D. Place Order (Save to DB)
    order = Order.objects.create(
        user=user,
        full_name=full_name,
        address=f"{random.randint(10,99)}, Gandhi Road, {random.choice(cities)}",
        city=random.choice(cities),
        state="Tamil Nadu",
        zipcode=f"6000{random.randint(10,99)}",
        phone=f"98765{random.randint(10000,99999)}",
        total_amount=total_bill,
        status="Pending"
    )

    # E. Add Items to Order
    for item in order_items:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            price=item['price'],
            quantity=item['qty']
        )

    print(f"✅ ORDER PLACED! Order #{order.id} | Amount: ₹{total_bill}")
    print("-" * 20)

print("🚀 SIMULATION COMPLETE! 5 New Orders Generated.")
print("👉 Go to Admin Panel (http://127.0.0.1:8000/admin/) to see them.")