import os

# PATHS
base_dir = os.getcwd()
store_dir = os.path.join(base_dir, 'store')
templates_dir = os.path.join(store_dir, 'templates', 'store')

print("-" * 40)
print("🚀 STARTING AMAZON UPGRADE (Design + Buy Button + Product Page)...")
print("-" * 40)

# ---------------------------------------------------------
# 1. UPDATE URLS (Add Product Page & Buy Now)
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
print("✅ URLs Updated (Product Page & Buy Now links added)")

# ---------------------------------------------------------
# 2. UPDATE VIEWS (Add Logic for New Features)
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
        # Simple Order Logic
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
print("✅ Views Updated (Buy Now Logic added)")

# ---------------------------------------------------------
# 3. CREATE PRODUCT DETAIL PAGE (Amazon Style)
# ---------------------------------------------------------
detail_html = """{% extends 'store/base.html' %}
{% block content %}
<div class="container mt-4 mb-5">
    <div class="row">
        <div class="col-md-5 text-center">
            <div class="border p-3" style="background: white;">
                <img src="{{ product.image_url }}" alt="{{ product.name }}" class="img-fluid" style="max-height: 400px; object-fit: contain;">
            </div>
        </div>

        <div class="col-md-4">
            <h2 style="font-weight: 600; color: #333;">{{ product.name }}</h2>
            <div class="mb-2">
                <span class="text-warning"><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star-half-stroke"></i></span>
                <span class="text-primary ms-2">{{ product.reviews_count }} ratings</span>
            </div>
            <hr>
            <h1 style="color: #B12704; font-weight: 500;">
                <span style="font-size: 16px; color: #565959; font-weight: 400;">Price:</span> 
                ₹{{ product.selling_price }}
            </h1>
            <p class="text-muted" style="text-decoration: line-through;">M.R.P.: ₹{{ product.original_price }}</p>
            
            <div class="mt-3">
                <h5>About this item</h5>
                <ul class="text-secondary small">
                    <li>High quality material and premium finish.</li>
                    <li>Best seller in category with top ratings.</li>
                    <li>Fast delivery available across India.</li>
                    <li>{{ product.description }}</li>
                </ul>
            </div>
        </div>

        <div class="col-md-3">
            <div class="card p-3 shadow-sm border-0" style="background: white;">
                <h4 class="text-danger">₹{{ product.selling_price }}</h4>
                <p class="text-success fw-bold small">In Stock.</p>
                <p class="small">Sold by <strong>Trendflix Retail</strong></p>
                
                <a href="{% url 'add_to_cart' product.id %}" class="btn btn-warning w-100 mb-2 rounded-pill" style="background-color: #ffd814; border-color: #fcd200;">Add to Cart</a>
                <a href="{% url 'buy_now' product.id %}" class="btn btn-warning w-100 rounded-pill" style="background-color: #fa8900; border-color: #ca6e00;">Buy Now</a>
                
                <div class="mt-3 small text-muted text-center">
                    <i class="fa-solid fa-lock"></i> Secure Transaction
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
with open(os.path.join(templates_dir, 'product_detail.html'), 'w', encoding='utf-8') as f:
    f.write(detail_html)
print("✅ Product Detail Page Created")

# ---------------------------------------------------------
# 4. UPDATE HOME.HTML (Amazon Grid + Buy Button)
# ---------------------------------------------------------
home_html = """{% extends 'store/base.html' %}

{% block content %}
<style>
    .hero-banner {
        background: url('https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?q=80&w=2070&auto=format&fit=crop');
        background-size: cover; background-position: center;
        height: 350px; display: flex; align-items: center; justify-content: center;
        width: 100%; position: relative;
    }
    .hero-gradient {
        position: absolute; bottom: 0; left: 0; right: 0; height: 100px;
        background: linear-gradient(to bottom, transparent, #eaeded);
    }
    
    .product-grid-container { padding: 20px; margin-top: -80px; position: relative; z-index: 10; }
    
    .product-card {
        background: white; border: 1px solid #ddd; padding: 15px; height: 100%;
        display: flex; flex-direction: column; justify-content: space-between;
    }
    .product-card:hover { transform: scale(1.01); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
    
    .product-link { text-decoration: none; color: inherit; }
    .product-img { max-height: 180px; object-fit: contain; margin-bottom: 10px; }
    
    .price { font-size: 21px; font-weight: 500; color: #B12704; }
    
    .btn-add { background-color: #ffd814; border: 1px solid #fcd200; border-radius: 20px; font-size: 13px; width: 48%; }
    .btn-buy { background-color: #fa8900; border: 1px solid #ca6e00; border-radius: 20px; font-size: 13px; width: 48%; }
</style>

<div class="hero-banner">
    <div class="hero-gradient"></div>
</div>

<div class="container-fluid product-grid-container">
    <div class="bg-white p-4 shadow-sm">
        <h3 class="mb-4 fw-bold">Up to 60% off | Best Sellers</h3>
        
        <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 row-cols-xl-5 g-3">
            {% for product in products %}
            <div class="col">
                <div class="product-card">
                    <a href="{% url 'product_detail' product.id %}" class="product-link">
                        <div class="text-center">
                            <img src="{{ product.image_url }}" class="product-img" alt="{{ product.name }}">
                        </div>
                        <h6 class="text-truncate mt-2 text-primary">{{ product.name }}</h6>
                        <div>
                            <span class="text-warning"><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i></span>
                            <span class="small text-muted">{{ product.reviews_count }}</span>
                        </div>
                        <div class="mt-1">
                            <span class="price">₹{{ product.selling_price }}</span>
                            <span class="text-muted small text-decoration-line-through">₹{{ product.original_price }}</span>
                        </div>
                    </a>
                    
                    <div class="d-flex justify-content-between mt-3">
                        <a href="{% url 'add_to_cart' product.id %}" class="btn btn-add">Add</a>
                        <a href="{% url 'buy_now' product.id %}" class="btn btn-buy">Buy Now</a>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}
"""
with open(os.path.join(templates_dir, 'home.html'), 'w', encoding='utf-8') as f:
    f.write(home_html)
print("✅ Home Page Updated (Buy Buttons Added)")

# ---------------------------------------------------------
# 5. UPDATE BASE.HTML (Full Width Layout)
# ---------------------------------------------------------
base_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trendflix | Online Shopping Site</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        :root { --primary-color: #131921; --accent-color: #febd69; --buy-color: #fa8900; }
        body { background-color: #eaeded; font-family: 'Inter', sans-serif; }
        .navbar { background-color: var(--primary-color) !important; padding: 10px 0; }
        .navbar-brand { font-weight: 800; font-size: 24px; color: white !important; }
        .nav-link { color: white !important; font-weight: 500; margin-left: 15px; }
        .search-box { border-radius: 4px 0 0 4px; border: none; }
        .search-btn { background-color: var(--accent-color); border: none; border-radius: 0 4px 4px 0; }
        .cart-badge { background-color: var(--buy-color); color: white; }
        footer { background-color: #232f3e; color: #ddd; padding: 40px 0; margin-top: 60px; text-align: center; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg sticky-top">
        <div class="container-fluid px-4">
            <a class="navbar-brand" href="/"><i class="fa-solid fa-bag-shopping text-warning"></i> TRENDFLIX</a>
            <button class="navbar-toggler bg-light" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"><span class="navbar-toggler-icon"></span></button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <form class="d-flex mx-auto" style="width: 50%;">
                    <input class="form-control search-box" type="search" placeholder="Search for products...">
                    <button class="btn search-btn" type="submit"><i class="fa-solid fa-magnifying-glass"></i></button>
                </form>
                <ul class="navbar-nav ms-auto align-items-center">
                    {% if user.is_authenticated %}
                        <li class="nav-item"><a href="#" class="nav-link">Hello, {{ user.username }}</a></li>
                        <li class="nav-item"><a href="{% url 'logout' %}" class="nav-link text-warning">Logout</a></li>
                    {% else %}
                        <li class="nav-item"><a href="{% url 'login' %}" class="nav-link">Login</a></li>
                    {% endif %}
                    <li class="nav-item">
                        <a href="{% url 'cart' %}" class="nav-link position-relative">
                            <i class="fa-solid fa-cart-shopping fa-lg"></i> Cart
                            <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill cart-badge">
                                {{ cart_count|default:"0" }}
                            </span>
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container-fluid px-0"> 
        {% block content %}{% endblock %}
    </div>

    <footer><div class="container"><p>&copy; 2025 Trendflix. All rights reserved.</p></div></footer>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
with open(os.path.join(templates_dir, 'base.html'), 'w', encoding='utf-8') as f:
    f.write(base_html)
print("✅ Base Layout Updated (Full Width)")

print("-" * 40)
print("🚀 SYSTEM UPGRADED! Run 'python manage.py runserver'")
print("-" * 40)