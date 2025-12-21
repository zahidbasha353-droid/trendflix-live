from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from store import views 

urlpatterns = [
    # --- 🏠 HOMEPAGE (Fixes 404 Error) ---
    path('', views.home, name='home'), 

    # --- 🛠️ ADMIN & AUTOMATION ---
    path('admin/', admin.site.urls),
    path('auto-update/<str:category_name>/', views.auto_update_products, name='auto_update_products'),

    # --- 🔑 AUTH PAGES ---
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # --- 👕 PRODUCT & CART ---
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # --- 💳 CHECKOUT & PAYMENT ---
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-success/', views.order_success_view, name='order_success_view'),
    
    # --- 📊 DASHBOARDS & CUSTOM DESIGN ---
    path('custom-design/', views.custom_design_view, name='custom_design'),
    path('dashboard/designer/', views.designer_dashboard, name='designer_dashboard'),
    path('upload-design/', views.upload_design, name='upload_design'),
    path('dashboard/owner/', views.owner_dashboard, name='owner_dashboard'),

    # --- 💱 CURRENCY SWITCHER ---
    path('switch-currency/<str:currency_code>/', views.switch_currency, name='switch_currency'),
]

# --- 💡 MEDIA & STATIC FILES CONFIG ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)