import os
import django
import time
import json
from datetime import datetime

# SETUP DJANGO
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trendflix_core.settings')
django.setup()

from store.models import Order

# CONFIG
SUPPLIER_FOLDER = "supplier_exports"
if not os.path.exists(SUPPLIER_FOLDER):
    os.makedirs(SUPPLIER_FOLDER)

def run_bot():
    print("=" * 60)
    print(f"🤖 TRENDFLIX AUTOMATION BOT | Started at {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)

    # 1. FIND PENDING ORDERS
    pending_orders = Order.objects.filter(status='Pending')
    
    if pending_orders.count() == 0:
        print("💤 No new orders. Bot is waiting...")
        return

    print(f"🔥 FOUND {pending_orders.count()} NEW ORDERS! Processing...\n")
    
    total_session_profit = 0

    for order in pending_orders:
        print(f"📦 Processing Order #{order.id} - {order.full_name}")
        
        order_items_data = []
        order_profit = 0
        
        # Calculate Costs & Profit
        for item in order.items.all():
            cost = item.product.cost_price
            sell = item.product.selling_price
            profit = (sell - cost) * item.quantity
            order_profit += profit
            
            order_items_data.append({
                "sku": item.product.sku,
                "name": item.product.name,
                "qty": item.quantity,
                "print_url": item.product.image_url # In real POD, this is the Design File
            })

        total_session_profit += order_profit

        # 2. GENERATE SUPPLIER FILE (JSON for API)
        supplier_payload = {
            "order_ref": f"ORD-{order.id}",
            "shipping": {
                "name": order.full_name,
                "address": order.address,
                "city": order.city,
                "zip": order.zipcode,
                "phone": order.phone
            },
            "items": order_items_data,
            "status": "READY_FOR_PRINT"
        }

        # Save File (Simulating API Call)
        filename = f"{SUPPLIER_FOLDER}/Order_{order.id}_Qikink.json"
        with open(filename, 'w') as f:
            json.dump(supplier_payload, f, indent=4)
            
        print(f"   ✅ Sent to Printing Dept (File: {filename})")
        print(f"   💰 Estimated Profit: ₹{order_profit}")

        # 3. UPDATE ORDER STATUS
        order.status = 'Processing' # Moved from Pending to Processing
        order.save()
        time.sleep(1) # Fake processing time

    print("-" * 60)
    print(f"💵 TOTAL PROFIT THIS SESSION: ₹{total_session_profit}")
    print("=" * 60)

if __name__ == "__main__":
    # In real life, use: while True: run_bot(); time.sleep(300)
    run_bot()