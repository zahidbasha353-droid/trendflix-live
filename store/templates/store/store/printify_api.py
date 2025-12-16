import requests
import json

# 🔥 YOUR REAL PRINTIFY TOKEN (Do not share this)
PRINTIFY_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzN2Q0YmQzMDM1ZmUxMWU5YTgwM2FiN2VlYjNjY2M5NyIsImp0aSI6ImI1NDM5Y2IzZjIyODUwOGQwMTk3NzUyYjYzOTIxNjI1NTNkZDMxMDQ1NGQxYWYxYWY2M2Q1ZTAwNmE3ZGFmYzQ3MGNmZjJjNTY2ODQzMjE3IiwiaWF0IjoxNzY1ODE5NDkwLjgyNjQ1NywibmJmIjoxNzY1ODE5NDkwLjgyNjQ1OCwiZXhwIjoxNzk3MzU1NDkwLjgxNjg1LCJzdWIiOiIyNTcxNjE3NyIsInNjb3BlcyI6WyJzaG9wcy5tYW5hZ2UiLCJzaG9wcy5yZWFkIiwiY2F0YWxvZy5yZWFkIiwib3JkZXJzLnJlYWQiLCJvcmRlcnMud3JpdGUiLCJwcm9kdWN0cy5yZWFkIiwicHJvZHVjdHMud3JpdGUiLCJ3ZWJob29rcy5yZWFkIiwid2ViaG9va3Mud3JpdGUiLCJ1cGxvYWRzLnJlYWQiLCJ1cGxvYWRzLndyaXRlIiwicHJpbnRfcHJvdmlkZXJzLnJlYWQiLCJ1c2VyLmluZm8iXX0.NYuRkmACFJI7dpxILoDjdj5-vrfId86sam5b2S5_l6fq9f54rt0vBQbZ75wzsO0vBX6VqhaE0cv-4J7yTMaDcvTtJeMRSJGuNTsA4_Nk6e6JXVn2ew0AZVm6Cpz1b7rkrrLXpL1FkNaIvWNNnEcj6lsTX_O_utDCZ0c3eyxltOjOZ-v6_vIKtSzu6zD_EQmKc9SwPArJ0ZyNMuwrIaPV2QszZ-d9s0CZGGD6hEfcvXoG2KcWjil-UGTTwZyjpDldY6mTr3FDJbjh2rHkCrCkayzaNDtbpQ-CNTiqR4QFhN2Jv3Rj-wI3Nvp1Jfue0zm491ZD6CPzNVGKCEJQ-0zGvX5khNFsfUQuTbI5pOI_BTRR4I9MFhgfqnNEaJmTMAaA0YE-NhUzYFBJAsIsZFhTuGGynjpXuur0WLcJSJuJFKELbgFCO8NK9XDkwA4Xc0c0k6DMusG59u5UPLogmSJHEI-H4JjY-Aut8ob4FNcPZMN2tLuq_GH2MSeqFk1X7o_w9YVIYCVoNxUgsN9cte2TmCBxiI8h6F0QfG4FiGNT1CH2W-HBCkaoCbN2QHn7yDp0e2W1yNOdefWF7hVN0ehugwygFbqpqdWObeLEkl6xStjk2V_JYoh5w4WpHZiHbYHXj4ccFTMl4umdEcv8WzCLVlHtvivtZfJUG9gmbWU34"

# 🛒 YOUR SHOP ID (Confirmed from screenshot)
SHOP_ID = "25702412"

API_URL = f"https://api.printify.com/v1/shops/{SHOP_ID}/orders.json"

def send_order_to_printify(order):
    """
    Sends order to Printify (Global)
    """
    print(f"✈️ Sending Order #{order.id} to Printify...")

    # 1. Prepare Items
    line_items = []
    for item in order.items.all():
        p_id = item.product.printify_product_id  
        v_id = item.product.printify_variant_id  
        
        if p_id and v_id:
            line_items.append({
                "product_id": p_id,
                "variant_id": int(v_id),
                "quantity": item.quantity
            })
        else:
            print(f"⚠️ Skipping {item.product.name} - No Printify ID found.")

    if not line_items:
        print("❌ No valid Printify items to sync.")
        return False

    # 2. Name Handling
    full_name_split = order.full_name.split()
    first_name = full_name_split[0]
    last_name = full_name_split[-1] if len(full_name_split) > 1 else ""

    # 3. Country Code Fix (India -> IN, etc.)
    country_code = order.country
    if country_code.lower() == "india": country_code = "IN"
    if country_code.lower() == "usa": country_code = "US"

    # 4. Payload
    payload = {
        "external_id": f"ORD-{order.id}",
        "label": f"TrendFlix Order #{order.id}",
        "shipping_method": 1, # Standard Shipping
        "send_shipping_notification": True,
        "address_to": {
            "first_name": first_name,
            "last_name": last_name,
            "email": order.user.email if order.user else "guest@trendflix.com",
            "phone": order.phone,
            "country": country_code,
            "region": order.state,
            "address1": order.address,
            "city": order.city,
            "zip": order.zipcode
        },
        "line_items": line_items
    }

    # 5. Send Request
    headers = {
        "Authorization": f"Bearer {PRINTIFY_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        
        # Save Response
        order.api_response = f"Printify: {response.status_code} - {response.text}"
        
        if response.status_code == 200:
            data = response.json()
            order.supplier_name = "Printify"
            order.supplier_order_id = data.get('id')
            order.save()
            print(f"✅ Success! Printify Order ID: {data.get('id')}")
            return True
        else:
            print(f"❌ Printify Failed: {response.text}")
            order.save()
            return False

    except Exception as e:
        print(f"⚠️ Printify Connection Error: {e}")
        return False