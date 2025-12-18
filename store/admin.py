from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
import csv
from .models import Product, Order, OrderItem, Cart, SavedDesign, Category, SiteSettings, HomeBanner

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
    list_display = ('name', 'selling_price', 'cost_price', 'profit', 'category', 'is_approved', 'is_trending', 'is_bestseller')
    list_filter = ('category', 'is_approved', 'is_trending', 'is_bestseller')
    search_fields = ('name', 'sku', 'category')
    list_editable = ('selling_price', 'is_approved', 'is_trending', 'is_bestseller')

# --- CATEGORY ADMIN ---
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_preview')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" style="border-radius:50px;" />'.format(obj.image.url))
        return "-"
    image_preview.short_description = "Image"

# --- BANNER ADMIN ---
@admin.register(HomeBanner)
class HomeBannerAdmin(admin.ModelAdmin):
    list_display = ('position', 'main_text', 'image_preview')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" style="border-radius:5px;" />'.format(obj.image.url))
        return "-"
    image_preview.short_description = "Preview"

# --- SITE SETTINGS ADMIN ---
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'active_theme')
    
    # Idhu mukkiyam: Oru vaati settings create pannita, thirumba "Add" button vara kudadhu
    def has_add_permission(self, request):
        if SiteSettings.objects.exists():
            return False
        return True

# --- OTHER SIMPLE REGISTRATIONS ---
admin.site.register(Cart)
admin.site.register(SavedDesign)