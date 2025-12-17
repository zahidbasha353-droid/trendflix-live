from django.urls import path
from . import views

urlpatterns = [
    # Base Pages
    path('', views.home, name='home'),
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
    path('dashboard/owner/', views.owner_dashboard, name='owner_dashboard'),
    path('upload-design/', views.upload_design, name='upload_design'),

    # 🔥 GLOBAL CURRENCY SWITCHER (New) 🔥
    path('switch-currency/<str:currency_code>/', views.switch_currency, name='switch_currency'),
]
from django.urls import path, include
from django.contrib import admin
from store.views import owner_dashboard  # <--- Import this

urlpatterns = [
    path('admin/dashboard/', owner_dashboard, name='owner_dashboard'), # <--- Add this line BEFORE admin.site.urls
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
]