import os

# 1. SETUP PATHS
base_dir = os.getcwd()
store_dir = os.path.join(base_dir, 'store')
templates_store_dir = os.path.join(store_dir, 'templates', 'store')
admin_path = os.path.join(store_dir, 'admin.py')

# Create Directories if missing
if not os.path.exists(templates_store_dir):
    os.makedirs(templates_store_dir)
    print(f"📁 Created directory: {templates_store_dir}")

print("-" * 50)
print("🔧 AUTO-FIXING DASHBOARD & ADMIN ERRORS...")
print("-" * 50)

# ==========================================
# 2. FIX DASHBOARD (NEW PRO DESIGN 🔥)
# ==========================================
dashboard_code = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Automation HQ | Trendflix Admin</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --bg-dark: #0f172a;
            --card-bg: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent-red: #e11d48;
            --accent-green: #10b981;
            --accent-blue: #3b82f6;
            --accent-yellow: #f59e0b;
        }

        body {
            background-color: var(--bg-dark);
            color: var(--text-main);
            font-family: 'Outfit', sans-serif;
            min-height: 100vh;
            padding-bottom: 50px;
        }

        /* NAVBAR */
        .dashboard-nav {
            background: rgba(30, 41, 59, 0.8);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid #334155;
            padding: 15px 30px;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .brand-logo { font-weight: 800; font-size: 24px; color: white; letter-spacing: -0.5px; }
        .brand-logo i { color: var(--accent-red); margin-right: 10px; }

        /* CARDS */
        .stat-card {
            background: var(--card-bg);
            border: 1px solid #334155;
            border-radius: 16px;
            padding: 25px;
            height: 100%;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.4);
            border-color: #475569;
        }

        /* TEXT STYLES */
        .label-text { font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; color: var(--text-muted); margin-bottom: 5px; }
        .value-text { font-size: 38px; font-weight: 800; color: white; line-height: 1.2; }
        .sub-text { font-size: 12px; color: var(--text-muted); margin-top: 5px; display: block;}

        /* MONEY CARD */
        .money-val { 
            background: -webkit-linear-gradient(45deg, #4ade80, #22c55e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* PIPELINE STATUS GRID */
        .pipeline-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .status-box {
            background: #1e293b;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            border: 1px solid #334155;
            position: relative;
        }
        .status-box::before {
            content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 4px; border-radius: 12px 12px 0 0;
        }
        .status-pending::before { background: var(--accent-yellow); }
        .status-processing::before { background: var(--accent-blue); }
        .status-shipped::before { background: #06b6d4; }
        .status-delivered::before { background: var(--accent-green); }
        .status-failed::before { background: var(--accent-red); }

        .status-icon { font-size: 24px; margin-bottom: 10px; opacity: 0.9; }
        .status-count { font-size: 28px; font-weight: 800; color: white; }
        .status-label { font-size: 12px; color: var(--text-muted); font-weight: 600; text-transform: uppercase; }

        /* BUTTONS */
        .btn-glow {
            background: var(--accent-red);
            color: white;
            border: none;
            padding: 10px 25px;
            border-radius: 50px;
            font-weight: 700;
            box-shadow: 0 0 20px rgba(225, 29, 72, 0.4);
            transition: 0.3s;
        }
        .btn-glow:hover { background: #be123c; box-shadow: 0 0 30px rgba(225, 29, 72, 0.6); color: white; }
    </style>
</head>
<body>

    <div class="dashboard-nav d-flex justify-content-between align-items-center">
        <div class="brand-logo"><i class="fa-solid fa-robot"></i> Trendflix HQ</div>
        <div>
            <span class="text-muted me-3 small d-none d-md-inline">Logged in as Owner</span>
            <a href="/" class="btn btn-outline-light btn-sm rounded-pill px-3 me-2">Visit Store</a>
            <a href="/admin/" class="btn btn-glow btn-sm">Manage Orders</a>
        </div>
    </div>

    <div class="container mt-5">
        
        <h5 class="text-muted fw-bold mb-4">BUSINESS SNAPSHOT</h5>
        <div class="row g-4">
            
            <div class="col-md-4">
                <div class="stat-card">
                    <div class="d-flex justify-content-between">
                        <div>
                            <div class="label-text">Total Revenue</div>
                            <div class="value-text">₹{{ total_revenue }}</div>
                            <span class="sub-text">Gross Sales (Lifetime)</span>
                        </div>
                        <i class="fa-solid fa-sack-dollar text-primary fs-1 opacity-25"></i>
                    </div>
                </div>
            </div>

            <div class="col-md-4">
                <div class="stat-card" style="border-color: rgba(16, 185, 129, 0.3);">
                    <div class="d-flex justify-content-between">
                        <div>
                            <div class="label-text" style="color: #6ee7b7;">Net Profit</div>
                            <div class="value-text money-val">₹{{ total_profit }}</div>
                            <span class="sub-text">Cash in Hand (Estimated)</span>
                        </div>
                        <i class="fa-solid fa-wallet text-success fs-1 opacity-25"></i>
                    </div>
                </div>
            </div>

            <div class="col-md-4">
                <div class="stat-card">
                    <div class="d-flex justify-content-between">
                        <div>
                            <div class="label-text">Orders Today</div>
                            <div class="value-text text-warning">{{ orders_today }}</div>
                            <span class="sub-text">New customers today</span>
                        </div>
                        <i class="fa-solid fa-calendar-day text-warning fs-1 opacity-25"></i>
                    </div>
                </div>
            </div>
        </div>

        <h5 class="text-muted fw-bold mb-4 mt-5">ORDER PIPELINE (LIVE)</h5>
        
        <div class="pipeline-grid">
            
            <div class="status-box status-pending">
                <i class="fa-solid fa-hourglass-start status-icon text-warning"></i>
                <div class="status-count">{{ pending_print }}</div>
                <div class="status-label">Pending Print</div>
            </div>

            <div class="status-box status-processing">
                <i class="fa-solid fa-print status-icon text-primary"></i>
                <div class="status-count">{{ in_production }}</div>
                <div class="status-label">Printing</div>
            </div>

            <div class="status-box status-shipped">
                <i class="fa-solid fa-truck-fast status-icon text-info"></i>
                <div class="status-count">{{ shipped }}</div>
                <div class="status-label">Shipped</div>
            </div>

            <div class="status-box status-delivered">
                <i class="fa-solid fa-check-circle status-icon text-success"></i>
                <div class="status-count">{{ delivered }}</div>
                <div class="status-label">Delivered</div>
            </div>

            <div class="status-box status-failed">
                <i class="fa-solid fa-triangle-exclamation status-icon text-danger"></i>
                <div class="status-count">{{ failed }}</div>
                <div class="status-label">Cancelled / RTO</div>
            </div>

        </div>

        <div class="mt-5 pt-4 border-top border-secondary">
            <div class="row text-muted small">
                <div class="col-md-6">
                    <strong>Total Products Live:</strong> <span class="text-white">{{ total_products }}</span> 
                    (Auto-Added by Bot: <span class="text-white">{{ auto_products }}</span>)
                </div>
                <div class="col-md-6 text-md-end">
                    System Status: <span class="text-success fw-bold">● Online</span>
                </div>
            </div>
        </div>

    </div>

</body>
</html>
"""

dashboard_path = os.path.join(templates_store_dir, 'owner_dashboard.html')
with open(dashboard_path, 'w', encoding='utf-8') as f:
    f.write(dashboard_code)

print(f"✅ FIXED: owner_dashboard.html created at: {dashboard_path}")

# ==========================================
# 3. FIX ADMIN PANEL (Standard Code)
# ==========================================
admin_code = """import csv
from django.http import HttpResponse
from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Order, OrderItem, Cart

# --- EXPORT FUNCTION ---
def export_to_supplier(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="supplier_orders.csv"'
    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Customer Name', 'Address', 'City', 'State', 'Zip', 'Phone', 'Product Name', 'SKU', 'Quantity', 'Design URL'])

    for order in queryset:
        for item in order.items.all():
            writer.writerow([
                f"ORD-{order.id}",
                order.full_name,
                order.address,
                order.city,
                order.state,
                order.zipcode,
                order.phone,
                item.product.name,
                item.product.sku,
                item.quantity,
                item.product.image_url
            ])
    return response

export_to_supplier.short_description = "📂 Export Selected for Supplier (Excel/CSV)"

# 1. PRODUCT ADMIN
class ProductAdmin(admin.ModelAdmin):
    list_display = ('image_view', 'name', 'selling_price', 'cost_price', 'profit_show', 'is_bestseller')
    list_editable = ('selling_price', 'cost_price', 'is_bestseller') 
    search_fields = ('name',)
    
    def image_view(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 5px; object-fit: cover;" />', obj.image_url)
        return "-"
    image_view.short_description = 'Image'

    def profit_show(self, obj):
        if obj.selling_price and obj.cost_price:
            profit = obj.selling_price - obj.cost_price
            color = "green" if profit > 0 else "red"
            return format_html('<span style="color:{}; font-weight:bold;">₹{}</span>', color, profit)
        return "-"
    profit_show.short_description = 'Profit'

# 2. ORDER ADMIN
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'status_view', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'id', 'phone')
    inlines = [OrderItemInline]
    actions = ['mark_as_dispatched', export_to_supplier]

    def status_view(self, obj):
        colors = { 
            'Pending': 'orange', 'Processing': 'blue', 'Dispatched': 'green', 'Cancelled': 'red', 'Delivered': 'purple'
        }
        color = colors.get(obj.status, 'grey')
        return format_html('<span style="color: white; background: {}; padding: 3px 10px; border-radius: 10px;">{}</span>', color, obj.status)
    status_view.short_description = 'Status'

    def mark_as_dispatched(self, request, queryset):
        queryset.update(status='Dispatched')
    mark_as_dispatched.short_description = "Mark selected orders as Dispatched"

# Register
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart)
"""

with open(admin_path, 'w', encoding='utf-8') as f:
    f.write(admin_code)

print("✅ FIXED: admin.py code corrected.")
print("-" * 50)
print("🚀 ALL ERRORS FIXED! Please Restart Server.")
print("-" * 50)