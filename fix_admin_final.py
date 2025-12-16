import os

# PATH SETUP
base_dir = os.getcwd()
store_dir = os.path.join(base_dir, 'store')
admin_path = os.path.join(store_dir, 'admin.py')

print("-" * 50)
print("🔧 FIXING ADMIN PANEL ERROR...")
print("-" * 50)

# CORRECT ADMIN CODE (Removed 'category' from list_filter)
admin_code = """from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Order, OrderItem, Cart

# 1. PRODUCT ADMIN
class ProductAdmin(admin.ModelAdmin):
    # REMOVED 'category' from list_filter to fix error
    list_display = ('image_tag', 'name', 'selling_price', 'original_price', 'rating', 'is_bestseller')
    list_editable = ('selling_price', 'is_bestseller') 
    search_fields = ('name', 'description')
    list_filter = ('is_bestseller',) # Fixed: Removed category
    
    def image_tag(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 5px;" />'.format(obj.image_url))
        return "-"
    image_tag.short_description = 'Image'

# 2. ORDER ITEMS
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

# 3. ORDER ADMIN
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'status_colored', 'total_amount', 'city', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'id', 'phone')
    inlines = [OrderItemInline]
    actions = ['mark_as_dispatched']

    def status_colored(self, obj):
        color = 'orange'
        if obj.status == 'Dispatched':
            color = 'green'
        elif obj.status == 'Delivered':
            color = 'blue'
        return format_html('<span style="color: white; background: {}; padding: 3px 10px; border-radius: 10px;">{}</span>', color, obj.status)
    status_colored.short_description = 'Status'

    def mark_as_dispatched(self, request, queryset):
        queryset.update(status='Dispatched')
    mark_as_dispatched.short_description = "Mark selected orders as Dispatched"

# Register Models
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart)
"""

with open(admin_path, 'w', encoding='utf-8') as f:
    f.write(admin_code)

print("✅ admin.py FIXED (Removed missing 'category' filter).")
print("-" * 50)
print("🚀 NOW RESTART SERVER: python manage.py runserver")
print("-" * 50)