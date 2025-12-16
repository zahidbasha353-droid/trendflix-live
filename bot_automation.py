import os
import django
import time
import requests
import json

# 1. SETUP DJANGO ENVIRONMENT
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trendflix_core.settings')
django.setup()

from store.models import Order, OrderItem

# --- 🔐 PRINTIFY CONFIGURATION ---
PRINTIFY_API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzN2Q0YmQzMDM1ZmUxMWU5YTgwM2FiN2VlYjNjY2M5NyIsImp0aSI6ImI1NDM5Y2IzZjIyODUwOGQwMTk3NzUyYjYzOTIxNjI1NTNkZDMxMDQ1NGQxYWYxYWY2M2Q1ZTAwNmE3ZGFmYzQ3MGNmZjJjNTY2ODQzMjE3IiwiaWF0IjoxNzY1ODE5NDkwLjgyNjQ1NywibmJmIjoxNzY1ODE5NDkwLjgyNjQ1OCwiZXhwIjoxNzk3MzU1NDkwLjgxNjg1LCJzdWIiOiIyNTcxNjE3NyIsInNjb3BlcyI6WyJzaG9wcy5tYW5hZ2UiLCJzaG9wcy5yZWFkIiwiY2F0YWxvZy5yZWFkIiwib3JkZXJzLnJlYWQiLCJvcmRlcnMud3JpdGUiLCJwcm9kdWN0cy5yZWFkIiwicHJvZHVjdHMud3JpdGUiLCJ3ZWJob29rcy5yZWFkIiwid2ViaG9va3Mud3JpdGUiLCJ1cGxvYWRzLnJlYWQiLCJ1cGxvYWRzLndyaXRlIiwicHJpbnRfcHJvdmlkZXJzLnJlYWQiLCJ1c2VyLmluZm8iXX0.NYuRkmACFJI7dpxILoDjdj5-vrfId86sam5b2S5_l6fq9f54rt0vBQbZ75wzsO0vBX6VqhaE0cv-4J7yTMaDcvTtJeMRSJGuNTsA4_Nk6e6JXVn2ew0AZVm6Cpz1b7rkrrLXpL1FkNaIvWNNnEcj6lsTX_O_utDCZ0c3eyxltOjOZ-v6_vIKtSzu6zD_EQmKc9SwPArJ0ZyNMuwrIaPV2QszZ-d9s0CZGGD6hEfcvXoG2KcWjil-UGTTwZyjpDldY6mTr3FDJbjh2rHkCrCkayzaNDtbpQ-CNTiqR4QFhN2Jv3Rj-wI3Nvp1Jfue0zm491ZD6CPzNVGKCEJQ-0zGvX5khNFsfUQuTbI5pOI_BTRR4I9MFhgfqnNEaJmTMAaA0YE-NhUzYFBJAsIsZFhTuGGynjpXuur0WLcJSJuJFKELbgFCO8NK9XDkwA4Xc0c0k6DMusG59u5UPLogmSJHEI-H4JjY-Aut8ob4FNcPZMN2tLuq_GH2MSeqFk1X7o_w9YVIYCVoNxUgsN9cte2TmCBxiI8h6F0QfG4FiGNT1CH2W-HBCkaoCbN2QHn7yDp0e2W1yNOdefWF7hVN0ehugwygFbqpqdWObeLEkl6xStjk2V_JYoh5w4WpHZiHbYHXj4ccFTMl4umdEcv8WzCLVlHtvivtZfJUG9gmbWU34"
PRINTIFY_SHOP_ID = "25702412"

# IMPORTANT: Test panrathuku, unga Printify account-la irukura
# Oru Real Product oda ID-a inga podunga.
TEST_PRODUCT_ID = "INGA_UNGA_PRINTIFY_PRODUCT_ID_PODUNGA" 

# Base URL
BASE_URL = f"https://api.printify.com/v1/shops/{PRINTIFY_SHOP_ID}"

print("-" * 50)
print("🤖 TRENDFLIX BOT: Printify (Global Mode)")
print("📡 Listening for 'Processing' orders...")
print("-" * 50)

while True:
    paid_orders = Order.objects.filter(status='Processing', supplier_order_id__isnull=True)

    if paid_orders.count() == 0:
        time.sleep(10)
        continue

    print(f"\n🔥 Found {paid_orders.count()} NEW PAID Orders! Processing...\n")

    for order in paid_orders:
        print(f"📦 Processing Order #{order.id} for {order.full_name}...")
        
        try:
            # 1. GET VARIANTS (Size Kandupidikka)
            # Namma 'Test Product ID' oda details-a Printify kitta irundhu edukurom
            headers = {"Authorization": f"Bearer {PRINTIFY_API_KEY}"}
            product_resp = requests.get(f"{BASE_URL}/products/694054165c97938d1e01a7e6.json", headers=headers)
            
            if product_resp.status_code != 200:
                print(f"   ❌ Error: Unga Test Product ID thappu! Check pannunga.")
                continue

            # Simple Logic: First available variant-a edu (Testing ku podhum)
            variants = product_resp.json().get('variants', [])
            if not variants:
                print("   ❌ Error: Indha product-la sizes ethum illa.")
                continue
                
            first_variant_id = variants[0]['id'] # Taking the first size (e.g., L or M)

            # 2. PREPARE PAYLOAD
            # Using the Test Product ID for ALL items in this order (For Proof of Concept)
            line_items = []
            for item in order.items.all():
                line_items.append({
                    "product_id": TEST_PRODUCT_ID,
                    "variant_id": first_variant_id,
                    "quantity": item.quantity
                })

            payload = {
                "external_id": f"ORD-{order.id}",
                "label": f"Order #{order.id} (Trendflix)",
                "shipping_method": 1, # Standard Shipping
                "send_shipping_notification": True,
                "address_to": {
                    "first_name": order.full_name.split()[0],
                    "last_name": order.full_name.split()[-1] if " " in order.full_name else "",
                    "address1": order.address,
                    "city": order.city,
                    "region": order.state, # Printify needs valid State code usually
                    "zip": order.zipcode,
                    "country": "IN" if order.country.lower() == "india" else "US", # Simple Map
                    "phone": order.phone,
                    "email": order.user.email if order.user else "guest@trendflix.com"
                },
                "line_items": line_items
            }

            # 3. SEND ORDER
            response = requests.post(f"{BASE_URL}/orders.json", json=payload, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                supplier_id = data.get('id')
                
                order.status = "Dispatched"
                order.supplier_name = "Printify"
                order.supplier_order_id = supplier_id
                order.save()
                
                print(f"   ✅ SUCCESS! Sent to Printify. Order ID: {supplier_id}")
            else:
                print(f"   ❌ Printify Error: {response.text}")

        except Exception as e:
            print(f"   ⚠️ ERROR: {e}")

    time.sleep(5)