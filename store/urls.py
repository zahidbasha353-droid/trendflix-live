from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    
    # Cart Actions
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    
    # 🔥 INDHA LINE ADD PANNITEN (Buy Now Button work aaga)
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),

    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Checkout & Order
    path('checkout/', views.checkout_view, name='checkout'),
    path('place-cod-order/', views.place_cod_order, name='place_cod_order'),
    path('order-success/', views.order_success_view, name='order_success'),
    
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    # Custom & Dashboards
    path('custom-design/', views.custom_design_view, name='custom_design'),
    path('dashboard/designer/', views.designer_dashboard, name='designer_dashboard'),
    path('dashboard/owner/', views.owner_dashboard, name='owner_dashboard'),
    path('upload-design/', views.upload_design, name='upload_design'),
]
path('order-success/', views.order_success_view, name='order_success_view'),