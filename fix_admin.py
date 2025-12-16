import os

# PATH SETUP
base_dir = os.getcwd()
store_dir = os.path.join(base_dir, 'store')
admin_file = os.path.join(store_dir, 'admin.py')

# NEW ADMIN CODE (Matches Checkout System)
admin_code = """from django.contrib import admin
from .models import Product, Order, OrderItem, Cart

# Product View
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'selling_price', 'sku', 'is_bestseller')
    search_fields = ('name', 'sku')

# Order Items (Shows products inside an order)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

# Order View (Updated for Checkout System)
class OrderAdmin(admin.ModelAdmin):
    # 'customer_name' removed, 'full_name' added
    list_display = ('id', 'full_name', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'address')
    inlines = [OrderItemInline]

# Register Models
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart)
"""

# WRITE FILE
with open(admin_file, 'w', encoding='utf-8') as f:
    f.write(admin_code)

print("-" * 30)
print("✅ ADMIN PANEL FIXED! Now database commands will work.")
print("-" * 30)