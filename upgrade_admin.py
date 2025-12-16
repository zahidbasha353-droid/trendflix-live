import os

# PATH SETUP
base_dir = os.getcwd()
store_dir = os.path.join(base_dir, 'store')
settings_path = os.path.join(base_dir, 'trendflix_core', 'settings.py')
admin_path = os.path.join(store_dir, 'admin.py')

print("-" * 50)
print("🚀 UPGRADING ADMIN PANEL TO 'JAZZMIN' THEME...")
print("-" * 50)

# ---------------------------------------------------------
# 1. UPDATE SETTINGS.PY (Add Jazzmin Theme)
# ---------------------------------------------------------
try:
    with open(settings_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    jazzmin_installed = False
    
    # Check if Jazzmin is already added to avoid duplicates
    content_str = "".join(lines)
    
    if "'jazzmin'" not in content_str and '"jazzmin"' not in content_str:
        for line in lines:
            # Insert Jazzmin BEFORE 'django.contrib.admin'
            if 'django.contrib.admin' in line and not jazzmin_installed:
                new_lines.append("    'jazzmin',\n")
                jazzmin_installed = True
            new_lines.append(line)
            
        # Add Jazzmin Config at the end
        jazzmin_config = """
# JAZZMIN SETTINGS (Admin UI)
JAZZMIN_SETTINGS = {
    "site_title": "Trendflix Admin",
    "site_header": "Trendflix",
    "site_brand": "Trendflix HQ",
    "welcome_sign": "Welcome to Trendflix Control Center",
    "copyright": "Trendflix Ltd",
    "search_model": "store.Order",
    "topmenu_links": [
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "View Site", "url": "/"},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "order_with_respect_to": ["store", "auth"],
    "icons": {
        "store.Product": "fas fa-tshirt",
        "store.Order": "fas fa-shipping-fast",
        "store.Cart": "fas fa-shopping-cart",
        "auth.User": "fas fa-users",
    },
}
"""
        new_lines.append(jazzmin_config)

        with open(settings_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print("✅ settings.py updated (Theme Installed).")
    else:
        print("ℹ️ Jazzmin already present in settings.py")

except Exception as e:
    print(f"❌ Error updating settings.py: {e}")


# ---------------------------------------------------------
# 2. UPDATE ADMIN.PY (Add Features: Images, Search, Filters)
# ---------------------------------------------------------
admin_code = """from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Order, OrderItem, Cart

# 1. PRODUCT ADMIN (With Images)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'name', 'selling_price', 'original_price', 'rating', 'is_bestseller')
    list_editable = ('selling_price', 'is_bestseller') # Edit price directly from list
    search_fields = ('name', 'description')
    list_filter = ('category', 'is_bestseller')
    
    # Function to show Image Thumbnail
    def image_tag(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 5px;" />'.format(obj.image_url))
        return "-"
    image_tag.short_description = 'Image'

# 2. ORDER ITEMS (Inline View)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

# 3. ORDER ADMIN (With Status Colors & Filters)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'status_colored', 'total_amount', 'city', 'created_at')
    list_filter = ('status', 'created_at') # Filter by Status (Pending/Dispatched)
    search_fields = ('full_name', 'id', 'phone')
    inlines = [OrderItemInline]
    actions = ['mark_as_dispatched']

    # Color code the status
    def status_colored(self, obj):
        color = 'orange'
        if obj.status == 'Dispatched':
            color = 'green'
        elif obj.status == 'Delivered':
            color = 'blue'
        return format_html('<span style="color: white; background: {}; padding: 3px 10px; border-radius: 10px;">{}</span>', color, obj.status)
    status_colored.short_description = 'Status'

    # Action Button
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

print("✅ admin.py updated (Features Added).")
print("-" * 50)
print("🚀 UPGRADE COMPLETE! Restart Server to see the Magic.")
print("-" * 50)