import os
import random
import string
import json
from django.conf import settings

# --- 1. AUTO-GENERATE PRINT FILE (Manifest) ---
def generate_print_manifest(order):
    """
    Creates a text file with order details for the printing team.
    In a real app, this would generate a High-Res PDF/PNG.
    """
    # Create 'media/print_files' directory if not exists
    base_dir = settings.BASE_DIR
    print_dir = os.path.join(base_dir, 'media', 'print_files')
    if not os.path.exists(print_dir):
        os.makedirs(print_dir)

    # File Content
    filename = f"MANIFEST_{order.id}_{order.full_name.replace(' ', '_')}.txt"
    filepath = os.path.join(print_dir, filename)
    
    content = f"""
    =========================================
    🖨️ TRENDFLIX PRINT MANIFEST - ORDER #{order.id}
    =========================================
    Customer: {order.full_name}
    Country:  {order.country}
    Shipping: {order.address}, {order.city}, {order.zipcode}
    -----------------------------------------
    ITEMS TO PRINT:
    """
    
    for item in order.items.all():
        content += f"\n[ ] {item.quantity} x {item.product.name} | Size: {getattr(item, 'size', 'M')} | SKU: {item.product.sku}"
    
    content += "\n\n========================================="
    
    # Save File
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return f"/media/print_files/{filename}"

# --- 2. SUPPLIER API HIT (Simulation) ---
def push_to_supplier(order):
    """
    Simulates sending data to Qikink (India) or Printify (Global).
    Returns: (Success Boolean, Tracking Number)
    """
    print(f"🤖 BOT: Analyzing Order #{order.id} for Country: {order.country}")

    # ROUTING LOGIC
    supplier = "UNKNOWN"
    if order.country.lower() == "india":
        supplier = "Qikink / Printrove"
    else:
        supplier = "Printify (Global)"

    print(f"🚀 BOT: Pushing Order to {supplier} API...")
    
    # SIMULATE API DELAY & RESPONSE
    # In real code: requests.post('https://api.qikink.com/order', json=data)
    
    # Auto-Generate Fake Tracking Number
    tracking_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    final_tracking = f"{supplier[:3].upper()}-{tracking_code}"
    
    print(f"✅ BOT: Success! Tracking ID Received: {final_tracking}")
    
    return True, final_tracking