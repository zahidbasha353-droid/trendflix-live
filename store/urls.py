from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from store.views import (
    home, product_detail, add_to_cart, cart_view, remove_from_cart, 
    buy_now, checkout_view, order_success_view, place_cod_order, # 🔥 Puthu COD view
    upload_design, designer_dashboard, owner_dashboard, 
    login_view, logout_view, register_view, custom_design_view, 
    save_custom_order, user_profile, reorder_item, save_user_design
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- MAIN PAGES ---
    path('', home, name='home'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('cart/', cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('buy-now/<int:product_id>/', buy_now, name='buy_now'),
    
    # --- CHECKOUT & ORDER ---
    path('checkout/', checkout_view, name='checkout'),           # 👈 Ithu than miss aachu!
    path('place-cod-order/', place_cod_order, name='place_cod_order'), # 🔥 COD Order Link
    path('order-success/', order_success_view, name='order_success_view'),
    
    # --- DASHBOARDS ---
    path('upload-design/', upload_design, name='upload_design'),
    path('designer-dashboard/', designer_dashboard, name='designer_dashboard'),
    path('owner-dashboard/', owner_dashboard, name='owner_dashboard'),
    
    # --- USER ACCOUNTS ---
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('profile/', user_profile, name='user_profile'),
    
    # --- CUSTOM TOOLS ---
    path('custom-design/', custom_design_view, name='custom_design'),
    path('save-custom-order/', save_custom_order, name='save_custom_order'),
    path('save-user-design/', save_user_design, name='save_user_design'),
    path('reorder/<int:product_id>/', reorder_item, name='reorder_item'),
]

# Media Files (Images) Setup
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)