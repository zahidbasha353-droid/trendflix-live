import csv
from django.http import HttpResponse
from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Order, OrderItem, Cart

# --- QC ACTION ---
def mark_qc_passed(modeladmin, request, queryset):
    queryset.update(qc_passed=True)
mark_qc_passed.short_description = "✅ Mark QC Passed"

# --- EXPORT ACTIONS ---
def export_india_orders(modeladmin, request, queryset):
    india_orders = queryset.filter(country__iexact='India')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="INDIA_ORDERS.csv"'
    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Name', 'Phone', 'Product', 'Qty'])
    for order in india_orders:
        for item in order.items.all():
            writer.writerow([f"ORD-{order.id}", order.full_name, order.phone, item.product.name, item.quantity])
    return response
export_india_orders.short_description = "🇮🇳 Export India Orders"

def export_global_orders(modeladmin, request, queryset):
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

# --- ADMIN CONFIG ---
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    # 🔥 ADDED 'tracking_number' TO DISPLAY
    list_display = ('id', 'full_name', 'country_flag', 'status', 'tracking_number', 'is_bulk_order')
    list_filter = ('country', 'status', 'is_bulk_order')
    inlines = [OrderItemInline]
    actions = ['mark_as_dispatched', mark_qc_passed, export_india_orders, export_global_orders]

    def country_flag(self, obj):
        return "🇮🇳 IND" if obj.country == 'India' else f"🌍 {obj.country}"
    
    def mark_as_dispatched(self, request, queryset):
        queryset.update(status='Dispatched')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'selling_price', 'cost_price')

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart)