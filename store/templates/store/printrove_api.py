import requests
import json

# 🔥 YOUR REAL PRINTROVE TOKEN (Do not share this)
PRINTROVE_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiNjJmNjEwY2ExM2MwNGZjNjE2MjlhOTVjZDk5ZWQzMjg4NmE1ZDYxMzU3OWE3ZjMxYWNmNjBmNGFhNTk1MDNiZDY2OWI0YWZmOTc0NTU4YTAiLCJpYXQiOjE3NjU4Nzc3MzguOTM2NzgsIm5iZiI6MTc2NTg3NzczOC45MzY3ODcsImV4cCI6MTc5NzQxMzczOC45Mjk2MzksInN1YiI6IjE3ODA0MiIsInNjb3BlcyI6W119.oGh3gAuCCEAM4tcSYZ9rLO5OgnUHMvHqqCunyJ3xXBJ-5nCQ5NjVTJ5DaF8ZilfdSf4Bro9xB85uIBOfaJ8bPjQeF1sg-Bjiy7o96NVXIXyclf0_2rnpSJdl5DKFIR6tf5jakRvdPUX1EgkiKtW5TPXzp96UV0IywwDwqvaK6wWWFEFUm5QlSNei5r5BTDQeQX9Zkhrx2nFvK8bfW9u-CG9vCNRJMz-bFqU1mdLg9KY0xdDVH3DwQqGiOtaL1SxplYchfeRq4rjBBGMvwFwXRUv61egleoBpJWBlx2iF_7U2pj7iDABcorQGRkvFftM8XazJL4Zn05afSvvHxVmoCEopAte5ZXZ1hwWbTM9j2yZIp_c3UmyvVM21n2d6UhOG4Kq_QZw2yrrxZALXvIy3DVNPWgBYln4Q-L0kFDsRBG24JYpJpmJwmwWG-aE59iUqluVQngC1QjTBk_yWqlAzHRy1pp6_55CBCD4BEbgdjIq6wJ_bibOB3trf28I-Ltu3OM4u_q97za5DtmaW2AV5Sc0hVG4hHoOZbtNwTkbN2HODmGhw1sKIMhGb9eCZbTHsvr7mSadPy9OEN99wrTobhJhbmy70sdZrGKw6Ktb-ssfg5-qoAssuEJJUG8XEaBe83Umj6KsDN2m5QAh2cbhZE75MlRvzn515gMmWzQwTfWA"

API_URL = "https://api.printrove.com/api/external/orders"

def send_order_to_printrove(order):
    """
    Sends order to Printrove (India)
    """
    print(f"🔄 Sending Order #{order.id} to Printrove...")

    # 1. Customer Details
    customer_data = {
        "name": order.full_name,
        "email": order.user.email if order.user else "guest@trendflix.com",
        "phone": order.phone,
        "address1": order.address,
        "city": order.city,
        "state": order.state,
        "pincode": order.zipcode,
        "country": "India"
    }

    # 2. Prepare Items
    order_items = []
    for item in order.items.all():
        # Get Variant ID from Product Model
        v_id = item.product.printrove_variant_id
        
        if v_id:
            order_items.append({
                "quantity": item.quantity,
                "variant_id": int(v_id), 
                "is_plain": False
            })
        else:
            print(f"⚠️ Skipping {item.product.name} - No Printrove ID found.")

    if not order_items:
        print("❌ No valid Printrove items to sync.")
        return False

    # 3. Final Payload
    payload = {
        "reference_number": f"ORD-{order.id}",
        "retail_price": int(order.total_amount),
        # If order is COD on your site, set cod=True. Here assuming you pay Printrove first.
        "cod": False, 
        "customer": customer_data,
        "order_products": order_items
    }

    # 4. Headers
    headers = {
        "Authorization": f"Bearer {PRINTROVE_TOKEN}",
        "Content-Type": "application/json"
    }

    # 5. Send Request
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        
        # Save Response for debugging
        order.api_response = f"Printrove: {response.status_code} - {response.text}"
        
        if response.status_code in [200, 201]:
            data = response.json()
            # Try to get order ID safely
            p_order_id = data.get('order_id') or data.get('id')
            
            order.supplier_name = "Printrove"
            order.supplier_order_id = p_order_id
            order.save()
            print(f"✅ Success! Printrove Order ID: {p_order_id}")
            return True
        else:
            print(f"❌ Printrove Failed: {response.text}")
            order.save()
            return False

    except Exception as e:
        print(f"⚠️ Printrove Connection Error: {e}")
        return False