from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
import csv
from .models import Product, Order, OrderItem, Cart, SavedDesign

# --- QC ACTION (Quality Check) ---
def mark_qc_passed(modeladmin, request, queryset):
    queryset.update(qc_passed=True)
mark_qc_passed.short_description = "✅ Mark QC Passed"

# --- EXPORT ACTIONS (India vs Global) ---
def export_india_orders(modeladmin, request, queryset):
    # Filter for India
    india_orders = queryset.filter(country__iexact='India')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="INDIA_ORDERS.csv"'
    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Name', 'Phone', 'Product', 'Qty', 'Price'])
    
    for order in india_orders:
        for item in order.items.all():
            writer.writerow([f"ORD-{order.id}", order.full_name, order.phone, item.product.name, item.quantity, item.price])
    return response
export_india_orders.short_description = "🇮🇳 Export India Orders"

def export_global_orders(modeladmin, request, queryset):
    # Filter for Non-India
    global_orders = queryset.exclude(country__iexact='India')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="GLOBAL_ORDERS.csv"'
    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Country', 'Name', 'Product', 'Qty'])
    
    for order in global_orders:
        for item in order.items.all():
            writer.writerow([f"ORD-{order.id}", order.country, order.full_name, item.product.name, item.quantity])
    return response
export_global_orders.short_description = "🌍 Export Global Orders"

# --- DISPATCH ACTION ---
def mark_as_dispatched(modeladmin, request, queryset):
    queryset.update(status='Dispatched')
mark_as_dispatched.short_description = "🚚 Mark as Dispatched"

# --- INLINE ITEMS (Order kulla items kaata) ---
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['price']

# --- ORDER ADMIN ---
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # 🔥 List Display Updated
    list_display = ('id', 'full_name', 'country_flag', 'total_amount', 'status', 'tracking_number', 'qc_passed')
    list_filter = ('country', 'status', 'qc_passed', 'created_at')
    search_fields = ('id', 'full_name', 'phone', 'tracking_number')
    inlines = [OrderItemInline]
    actions = [mark_as_dispatched, mark_qc_passed, export_india_orders, export_global_orders]

    def country_flag(self, obj):
        return "🇮🇳 IND" if obj.country.lower() == 'india' else f"🌍 {obj.country}"
    country_flag.short_description = "Country"

# --- PRODUCT ADMIN ---
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # 🔥 FIXED: Matching New Models.py
    # Removed 'slug', changed 'price' -> 'selling_price', 'is_active' -> 'is_approved'
    list_display = ('name', 'selling_price', 'cost_price', 'profit', 'category', 'is_approved', 'is_trending', 'is_bestseller')
    list_filter = ('category', 'is_approved', 'is_trending', 'is_bestseller')
    search_fields = ('name', 'sku', 'category')
    list_editable = ('selling_price', 'is_approved', 'is_trending', 'is_bestseller')
    
    # Optional: Display Image thumbnail in Admin (Advanced)
    # def image_tag(self, obj):
    #     return format_html('<img src="{}" width="50" height="50" />'.format(obj.image.url)) if obj.image else "-"

# --- OTHER REGISTRATIONS ---
admin.site.register(Cart)
admin.site.register(SavedDesign)
# --- SITE SETTINGS (Dynamic Logo, Banner & Themes) ---
class SiteSettings(models.Model):
    THEME_CHOICES = [
        ('default', 'Default (No Effect)'),
        ('christmas', '❄️ Christmas / New Year (Snow)'),
        ('diwali', '🪔 Diwali / Eid (Golden Lights)'),
        ('sale', '🎉 Big Sale (Confetti)'),
    ]

    site_name = models.CharField(max_length=100, default="TrendFlix")
    logo = models.ImageField(upload_to='site_assets/', help_text="Upload transparent PNG logo")
    hero_banner = models.ImageField(upload_to='site_assets/', help_text="Main Home Banner (1920x600)")
    
    # Festival Mode
    active_theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='default')
    
    def __str__(self):
        return "Website Configuration"

    class Meta:
        verbose_name_plural = "Site Settings"