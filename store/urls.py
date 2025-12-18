from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from store import views  # <--- Ithu romba mukkiyam!

urlpatterns = [
    # --- ADMIN PANEL ---
    path('admin/', admin.site.urls),

    # --- HOMEPAGE (Idhu thaan 404 error fix pannum) ---
    path('', views.home, name='home'),

    # --- OTHER PAGES (Unga Old Coding) ---
    path('custom-design/', views.custom_design_view, name='custom_design'),
    
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # Product Flow
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Checkout & Payment
    path('checkout/', views.checkout_view, name='checkout'),
    path('place-cod-order/', views.place_cod_order, name='place_cod_order'), 
    
    # Success Page
    path('order-success/', views.order_success_view, name='order_success_view'),

    # Dashboards & Uploads
    path('dashboard/designer/', views.designer_dashboard, name='designer_dashboard'),
    path('upload-design/', views.upload_design, name='upload_design'),
    path('dashboard/owner/', views.owner_dashboard, name='owner_dashboard_app'),

    # Global Currency Switcher
    path('switch-currency/<str:currency_code>/', views.switch_currency, name='switch_currency'),
]

# --- MEDIA & STATIC FILES SETTINGS (Images Load Aaga) ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)