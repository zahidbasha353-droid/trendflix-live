import os

# PATHS
base_dir = os.getcwd()
store_dir = os.path.join(base_dir, 'store')
templates_dir = os.path.join(store_dir, 'templates', 'store')

# ---------------------------------------------------------
# 1. UPDATE MODELS (Database for Cart)
# ---------------------------------------------------------
models_code = """from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(max_length=500)
    sku = models.CharField(max_length=50, unique=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    reviews_count = models.IntegerField(default=100)
    is_bestseller = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.selling_price * self.quantity

class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50, default='Pending')
    order_date = models.DateTimeField(auto_now_add=True)
"""
with open(os.path.join(store_dir, 'models.py'), 'w', encoding='utf-8') as f:
    f.write(models_code)
print("✅ Models Updated (Cart Added)")

# ---------------------------------------------------------
# 2. UPDATE URLS (Links for Add/Remove)
# ---------------------------------------------------------
urls_code = """from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]
"""
with open(os.path.join(store_dir, 'urls.py'), 'w', encoding='utf-8') as f:
    f.write(urls_code)
print("✅ URLs Updated")

# ---------------------------------------------------------
# 3. UPDATE VIEWS (Logic for Cart)
# ---------------------------------------------------------
views_code = """from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product, Cart, CartItem

# Helper: Get or Create Cart
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
    cart_count = cart.items.count()
    return render(request, 'store/home.html', {'products': products, 'cart_count': cart_count})

def cart_view(request):
    cart = _get_cart(request)
    return render(request, 'store/cart.html', {'cart': cart, 'cart_count': cart.items.count()})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('home')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart')

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

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')
"""
with open(os.path.join(store_dir, 'views.py'), 'w', encoding='utf-8') as f:
    f.write(views_code)
print("✅ Views Updated (Logic Added)")

# ---------------------------------------------------------
# 4. CREATE CART HTML (The Cart Page)
# ---------------------------------------------------------
cart_html = """{% extends 'store/base.html' %}
{% block content %}
<div class="container">
    <h2 class="mb-4">Shopping Cart</h2>
    {% if cart.items.all %}
    <div class="card p-3 shadow-sm">
        <table class="table">
            <thead>
                <tr>
                    <th>Product</th>
                    <th>Price</th>
                    <th>Quantity</th>
                    <th>Total</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                {% for item in cart.items.all %}
                <tr>
                    <td>
                        <img src="{{ item.product.image_url }}" style="height: 50px; width: 50px; object-fit: contain;">
                        {{ item.product.name }}
                    </td>
                    <td>₹{{ item.product.selling_price }}</td>
                    <td>{{ item.quantity }}</td>
                    <td>₹{{ item.total_price }}</td>
                    <td>
                        <a href="{% url 'remove_from_cart' item.id %}" class="btn btn-sm btn-danger"><i class="fa-solid fa-trash"></i></a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        <div class="text-end mt-3">
            <h4>Subtotal: ₹{{ cart.total_price }}</h4>
            <button class="btn btn-warning btn-lg mt-2">Proceed to Checkout</button>
        </div>
    </div>
    {% else %}
    <div class="alert alert-info">Your cart is empty. <a href="{% url 'home' %}">Continue Shopping</a></div>
    {% endif %}
</div>
{% endblock %}
"""
with open(os.path.join(templates_dir, 'cart.html'), 'w', encoding='utf-8') as f:
    f.write(cart_html)
print("✅ Cart Page Created")

# ---------------------------------------------------------
# 5. UPDATE HOME HTML (Enable Buttons)
# ---------------------------------------------------------
home_html = """{% extends 'store/base.html' %}
{% block content %}
<style>
    .hero-banner { background: linear-gradient(to right, #2c3e50, #4ca1af); color: white; padding: 40px; border-radius: 20px; margin-bottom: 40px; text-align: center; box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
    .product-card { border: none; background: white; border-radius: 15px; overflow: hidden; transition: transform 0.3s; box-shadow: 0 5px 15px rgba(0,0,0,0.05); height: 100%; }
    .product-card:hover { transform: translateY(-5px); }
    .product-img-container { height: 250px; background: #f4f4f4; display: flex; align-items: center; justify-content: center; position: relative; }
    .product-img { max-height: 200px; max-width: 90%; object-fit: contain; }
    .card-body { padding: 20px; }
    .price { font-size: 18px; font-weight: bold; color: #2c3e50; }
    .btn-cart { background-color: #2c3e50; color: white; width: 100%; border-radius: 10px; padding: 10px; margin-top: 10px; text-decoration: none; display: block; text-align: center; }
    .btn-cart:hover { background-color: #e74c3c; color: white; }
</style>

<div class="hero-banner">
    <h1>Welcome to Trendflix</h1>
    <p>Discover the latest trends in fashion.</p>
</div>

<h3 class="mb-4">Latest Arrivals</h3>
<div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4">
    {% for product in products %}
    <div class="col">
        <div class="product-card">
            <div class="product-img-container">
                <img src="{{ product.image_url }}" class="product-img" alt="{{ product.name }}">
            </div>
            <div class="card-body">
                <h5 class="text-truncate">{{ product.name }}</h5>
                <div class="price">₹{{ product.selling_price }}</div>
                <a href="{% url 'add_to_cart' product.id %}" class="btn btn-cart">Add to Cart</a>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}
"""
with open(os.path.join(templates_dir, 'home.html'), 'w', encoding='utf-8') as f:
    f.write(home_html)
print("✅ Home Page Updated (Buttons Active)")

# ---------------------------------------------------------
# 6. UPDATE BASE HTML (Cart Count)
# ---------------------------------------------------------
base_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trendflix | Premium Store</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { --primary-color: #2c3e50; --accent-color: #e74c3c; }
        body { background-color: #f8f9fa; font-family: 'Poppins', sans-serif; }
        .navbar { background: white !important; box-shadow: 0 2px 10px rgba(0,0,0,0.05); padding: 15px 0; }
        .navbar-brand { color: var(--primary-color) !important; font-weight: 700; font-size: 26px; }
        .nav-link { color: #555 !important; font-weight: 500; margin-left: 20px; }
        .nav-link:hover { color: var(--accent-color) !important; }
        footer { background-color: #1a252f; color: #bdc3c7; padding: 40px 0; margin-top: 60px; text-align: center; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg sticky-top">
        <div class="container">
            <a class="navbar-brand" href="/"><i class="fa-solid fa-bag-shopping text-danger"></i> TRENDFLIX</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"><span class="navbar-toggler-icon"></span></button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto align-items-center">
                    {% if user.is_authenticated %}
                        <li class="nav-item"><a href="#" class="nav-link"><i class="fa-regular fa-user"></i> {{ user.username }}</a></li>
                        <li class="nav-item"><a href="{% url 'logout' %}" class="nav-link text-danger">Logout</a></li>
                    {% else %}
                        <li class="nav-item"><a href="{% url 'login' %}" class="nav-link">Login</a></li>
                    {% endif %}
                    <li class="nav-item">
                        <a href="{% url 'cart' %}" class="nav-link position-relative">
                            <i class="fa-solid fa-cart-shopping fa-lg"></i>
                            <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                                {{ cart_count|default:"0" }}
                            </span>
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    <div class="container mt-4">
        {% block content %}{% endblock %}
    </div>
    <footer><div class="container text-center"><p>&copy; 2025 Trendflix. All rights reserved.</p></div></footer>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
with open(os.path.join(templates_dir, 'base.html'), 'w', encoding='utf-8') as f:
    f.write(base_html)
print("✅ Navbar Updated (Cart Count Active)")

print("-" * 30)
print("🚀 READY FOR DATABASE UPDATE!")
print("Now run: python manage.py makemigrations")
print("Then run: python manage.py migrate")
print("-" * 30)