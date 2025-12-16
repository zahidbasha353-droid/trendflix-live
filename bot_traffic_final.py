import os
import django
import random
import datetime

# 1. SETUP DJANGO ENVIRONMENT
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trendflix_core.settings')
django.setup()

from django.contrib.auth.models import User
from store.models import Product, Order, OrderItem

# 2. SIMPLE DATA (No Faker Library Needed)
first_names = ["Rahul", "Priya", "Ahmed", "Anita", "Suresh", "Divya", "Karthik", "Meera", "Vikram", "Sneha", "Ravi", "Lakshmi"]
last_names = ["Kumar", "Sharma", "Khan", "Reddy", "Nair", "Patel", "Singh", "Das", "Rao", "Basha", "Krishnan", "Menon"]
cities = ["Chennai", "Mumbai", "Bangalore", "Delhi", "Hyderabad", "Coimbatore", "Madurai", "Trichy", "Salem"]
streets = ["Gandhi Road", "Anna Nagar", "MG Road", "Church Street", "Station Road", "North Street"]

print("-" * 40)
print("🤖 TRAFFIC BOT STARTED: Generating Orders...")
print("-" * 40)

# 3. GET PRODUCTS
products = list(Product.objects.all())
if not products:
    print("❌ Error: Kadai Kaaliya Irukku! Run 'bot_inventory.py' first.")
    exit()

# 4. CREATE 10 ORDERS
for i in range(1, 11):
    # A. Generate Random Customer
    fname = random.choice(first_names)
    lname = random.choice(last_names)
    username = f"{fname.lower()}{random.randint(100,999)}"
    email = f"{username}@example.com"
    full_name = f"{fname} {lname}"
    
    # Create User
    user, created = User.objects.get_or_create(username=username, email=email)
    if created:
        user.set_password("pass123")
        user.save()

    # B. Select Products
    num_items = random.randint(1, 4)
    selected_products = random.sample(products, num_items)
    
    total_bill = 0
    order_items_data = []

    # C. Calculate Total
    for product in selected_products:
        qty = random.randint(1, 2)
        total_bill += (product.selling_price * qty)
        order_items_data.append({'product': product, 'qty': qty, 'price': product.selling_price})

    # D. Create Order
    order = Order.objects.create(
        user=user,
        full_name=full_name,
        address=f"{random.randint(1,100)}, {random.choice(streets)}",
        city=random.choice(cities),
        state="Tamil Nadu",
        zipcode=f"600{random.randint(100,999)}",
        phone=f"98765{random.randint(10000,99999)}",
        total_amount=total_bill,
        status="Pending"
    )

    # E. Add Items
    for item in order_items_data:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            price=item['price'],
            quantity=item['qty']
        )

    print(f"💰 Order #{order.id} Placed by {full_name} | Bill: ₹{total_bill}")

print("-" * 40)
print("🚀 SUCCESS! 10 New Orders added.")
print("👉 Check Admin Panel now: http://127.0.0.1:8000/admin/")
print("-" * 40)