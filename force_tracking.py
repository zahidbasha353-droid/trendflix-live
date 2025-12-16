import os
import django

# 1. SETUP DJANGO
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trendflix_core.settings') # Check folder name!
django.setup()

from store.models import Order
from store.utils import push_to_supplier

def force_run_bot():
    print("-" * 50)
    print("🤖 MANUAL BOT TRIGGER STARTED...")
    print("-" * 50)

    # Get the latest order (Last one created)
    try:
        last_order = Order.objects.latest('created_at')
        print(f"📦 Found Last Order: #{last_order.id} - {last_order.full_name}")
        
        if last_order.tracking_number:
            print(f"⚠️ Tracking ID Already Exists: {last_order.tracking_number}")
            choice = input("Overwrite? (y/n): ")
            if choice.lower() != 'y':
                return

        # RUN THE BOT MANUALLY
        print("🚀 Calling Supplier API (Simulation)...")
        success, tracking_id = push_to_supplier(last_order)

        if success:
            last_order.tracking_number = tracking_id
            last_order.status = "Dispatched"
            last_order.save()
            print(f"✅ SUCCESS! Tracking ID Updated: {tracking_id}")
            print(f"🚚 Order Status Changed to: Dispatched")
        else:
            print("❌ Failed to generate tracking.")

    except Order.DoesNotExist:
        print("❌ No orders found in database!")

if __name__ == "__main__":
    force_run_bot()