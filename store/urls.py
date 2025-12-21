from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from store import views  # store app views-ah import panrom

urlpatterns = [
    # --- ADMIN PANEL ---
    path('admin/', admin.site.urls),

    # --- HOMEPAGE ---
    path('', views.home, name='home'),

    # --- AUTH PAGES ---
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # --- PRODUCT FLOW ---
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # --- CHECKOUT & PAYMENT ---
    path('checkout/', views.checkout_view, name='checkout_view'),
    path('order-success/', views.order_success_view, name='order_success_view'),
    
    # --- DASHBOARDS & CUSTOM DESIGN ---
    path('custom-design/', views.custom_design_view, name='custom_design'),
    path('dashboard/designer/', views.designer_dashboard, name='designer_dashboard'),
    path('upload-design/', views.upload_design, name='upload_design'),
    path('dashboard/owner/', views.owner_dashboard, name='owner_dashboard'),

    # --- GLOBAL CURRENCY SWITCHER ---
    path('switch-currency/<str:currency_code>/', views.switch_currency, name='switch_currency'),
]

# --- 💡 MEDIA & STATIC FILES (Hero Banners Load Aaga Idhu Romba Mukkiyam) ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # trendflix_core/urls.py

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    
    # Inga dhaan prachanai - 'order_success_view' nu function irukanum
    path('order-success/', views.order_success_view, name='order_success_view'),
    
    path('custom-design/', views.custom_design_view, name='custom_design'),
    path('dashboard/designer/', views.designer_dashboard, name='designer_dashboard'),
    path('upload-design/', views.upload_design, name='upload_design'),
    path('dashboard/owner/', views.owner_dashboard, name='owner_dashboard'),
    path('switch-currency/<str:currency_code>/', views.switch_currency, name='switch_currency'),
    
]
from django.urls import path
from . import views

urlpatterns = [
    # ... unga matha paths ...
    path('auto-update/<str:category_name>/', views.auto_update_products, name='auto_update_products'),
]