import os

# PATHS
base_dir = os.getcwd()
store_dir = os.path.join(base_dir, 'store')
templates_dir = os.path.join(store_dir, 'templates', 'store')

print("-" * 40)
print("🎨 DESIGNING PREMIUM PRODUCT PAGE (Amazon Reference Style)...")
print("-" * 40)

# ---------------------------------------------------------
# 1. UPDATE PRODUCT DETAIL HTML (The Main Design)
# ---------------------------------------------------------
detail_html = """{% extends 'store/base.html' %}
{% block content %}
<style>
    /* Page Layout */
    .product-container {
        background-color: white;
        padding: 30px;
        margin-top: 20px;
    }

    /* Left: Image Section */
    .img-container {
        position: sticky;
        top: 100px;
        text-align: center;
    }
    .main-img {
        max-width: 100%;
        max-height: 500px;
        object-fit: contain;
    }

    /* Center: Product Info */
    .product-title {
        font-size: 24px;
        font-weight: 600;
        color: #333;
        line-height: 1.3;
    }
    .rating-section {
        margin-bottom: 15px;
        font-size: 14px;
    }
    .price-tag {
        font-size: 28px;
        font-weight: 500;
        color: #B12704; /* Amazon Price Red */
    }
    .mrp-tag {
        text-decoration: line-through;
        color: #565959;
        font-size: 14px;
    }
    .feature-list {
        margin-top: 20px;
    }
    .feature-list li {
        margin-bottom: 8px;
        color: #333;
        font-size: 14px;
    }

    /* Right: Buy Box (Card) */
    .buy-box {
        border: 1px solid #d5d9d9;
        border-radius: 8px;
        padding: 20px;
        background-color: white;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .stock-status {
        color: #007600;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 15px;
    }
    
    /* Buttons */
    .btn-cart-custom {
        background-color: #ffd814;
        border-color: #fcd200;
        color: #111;
        border-radius: 20px;
        font-weight: 500;
        width: 100%;
        margin-bottom: 10px;
    }
    .btn-cart-custom:hover { background-color: #f7ca00; }

    .btn-buy-custom {
        background-color: #fa8900;
        border-color: #ca6e00;
        color: #111;
        border-radius: 20px;
        font-weight: 500;
        width: 100%;
    }
    .btn-buy-custom:hover { background-color: #e37b00; }

    .secure-text {
        font-size: 13px;
        color: #007185;
        margin-top: 15px;
        text-align: center;
        cursor: pointer;
    }
    .secure-text:hover { color: #c7511f; text-decoration: underline; }
</style>

<div class="container-fluid product-container">
    <div class="row">
        <div class="col-md-5">
            <div class="img-container">
                <img src="{{ product.image_url }}" alt="{{ product.name }}" class="main-img">
            </div>
        </div>

        <div class="col-md-4">
            <h1 class="product-title">{{ product.name }}</h1>
            
            <div class="rating-section">
                <span class="text-warning">
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-solid fa-star"></i>
                    <i class="fa-solid fa-star-half-stroke"></i>
                </span>
                <span class="text-primary ms-2">{{ product.reviews_count }} ratings</span>
                <span class="text-muted"> | 1K+ bought in past month</span>
            </div>

            <hr style="opacity: 0.1;">

            <div class="mb-3">
                <span class="mrp-tag">M.R.P.: ₹{{ product.original_price }}</span>
                <div class="price-tag">
                    <sup style="font-size: 14px; top: -0.5em;">₹</sup>{{ product.selling_price }}
                </div>
                <span class="badge bg-danger">Deal of the Day</span>
            </div>

            <div class="feature-list">
                <h6 class="fw-bold">About this item</h6>
                <ul>
                    <li>{{ product.description }}</li>
                    <li>High quality premium finish with durable material.</li>
                    <li>Best in class performance and top rated by users.</li>
                    <li>Comes with Trendflix brand warranty.</li>
                    <li>Fast and secure delivery across India.</li>
                </ul>
            </div>
        </div>

        <div class="col-md-3">
            <div class="buy-box">
                <h3 class="fw-bold mb-1">₹{{ product.selling_price }}</h3>
                <div class="stock-status">In Stock</div>
                
                <p class="small text-muted mb-3">
                    Ships from: <strong>Trendflix</strong><br>
                    Sold by: <strong>Trendflix Retail</strong>
                </p>

                <div class="d-grid gap-2">
                    <a href="{% url 'add_to_cart' product.id %}" class="btn btn-cart-custom">Add to Cart</a>
                    <a href="{% url 'buy_now' product.id %}" class="btn btn-buy-custom">Buy Now</a>
                </div>

                <div class="secure-text">
                    <i class="fa-solid fa-lock"></i> Secure transaction
                </div>

                <hr class="my-3">
                
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" checked>
                    <label class="form-check-label small text-muted">Add gift options</label>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
with open(os.path.join(templates_dir, 'product_detail.html'), 'w', encoding='utf-8') as f:
    f.write(detail_html)
print("✅ Product Detail Page Designed (Amazon Layout)")

# ---------------------------------------------------------
# 2. UPDATE URLS (Ensure 'buy_now' exists)
# ---------------------------------------------------------
urls_code = """from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-success/', views.order_success_view, name='order_success'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]
"""
with open(os.path.join(store_dir, 'urls.py'), 'w', encoding='utf-8') as f:
    f.write(urls_code)
print("✅ URLs Updated")

# ---------------------------------------------------------
# 3. UPDATE VIEWS (Logic for Page & Buttons)
# ---------------------------------------------------------
views_code = """from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product, Cart, CartItem, Order, OrderItem

def _get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    return cart

def home(request):
    products = Product.objects.all()
    cart = _get_cart(request)
    return render(request, 'store/home.html', {'products': products, 'cart_count': cart.items.count()})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_cart(request)
    return render(request, 'store/product_detail.html', {'product': product, 'cart_count': cart.items.count()})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('home')

def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_cart(request)
    # Clear cart first for Buy Now (Optional, but good for direct checkout)
    # cart.items.all().delete() 
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('checkout')

def cart_view(request):
    cart = _get_cart(request)
    return render(request, 'store/cart.html', {'cart': cart, 'cart_count': cart.items.count()})

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart')

def checkout_view(request):
    cart = _get_cart(request)
    if cart.items.count() == 0:
        return redirect('home')
    if request.method == 'POST':
        Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=request.POST.get('full_name'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            zipcode=request.POST.get('zipcode'),
            phone=request.POST.get('phone'),
            total_amount=cart.total_price
        )
        cart.items.all().delete()
        return redirect('order_success')
    return render(request, 'store/checkout.html', {'cart': cart, 'cart_count': cart.items.count()})

def order_success_view(request):
    return render(request, 'store/order_success.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})
"""
with open(os.path.join(store_dir, 'views.py'), 'w', encoding='utf-8') as f:
    f.write(views_code)
print("✅ Views Logic Updated")

print("-" * 40)
print("🚀 PRODUCT PAGE UPGRADED! Refresh website & Click a product.")
print("-" * 40)