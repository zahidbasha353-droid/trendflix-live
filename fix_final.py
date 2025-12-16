import os

# 1. SETUP PATHS
base_dir = os.getcwd()
store_dir = os.path.join(base_dir, 'store')
templates_dir = os.path.join(store_dir, 'templates', 'store')

# ---------------------------------------------------------
# FILE 1: URLS.PY (Fixing "NoReverseMatch" - Login Links)
# ---------------------------------------------------------
urls_content = """from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]
"""
with open(os.path.join(store_dir, 'urls.py'), 'w', encoding='utf-8') as f:
    f.write(urls_content)
print("✅ FIXED: urls.py (Login links connected)")

# ---------------------------------------------------------
# FILE 2: VIEWS.PY (Adding Login Logic)
# ---------------------------------------------------------
views_content = """from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product

def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

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
    f.write(views_content)
print("✅ FIXED: views.py (Login logic added)")

# ---------------------------------------------------------
# FILE 3: HOME.HTML (Fixing "floatform" error & Design)
# ---------------------------------------------------------
home_html_content = """{% extends 'store/base.html' %}

{% block content %}
<style>
    .hero-banner {
        background: linear-gradient(to right, #2c3e50, #4ca1af);
        color: white; padding: 40px; border-radius: 20px;
        margin-bottom: 40px; text-align: center;
    }
    .product-card {
        border: none; background: white; border-radius: 15px;
        overflow: hidden; transition: transform 0.3s;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05); height: 100%;
    }
    .product-card:hover { transform: translateY(-5px); }
    .product-img-container {
        height: 250px; background: #f4f4f4; display: flex;
        align-items: center; justify-content: center; position: relative;
    }
    .product-img { max-height: 200px; max-width: 90%; object-fit: contain; }
    .card-body { padding: 20px; }
    .price { font-size: 18px; font-weight: bold; color: #2c3e50; }
    .btn-cart {
        background-color: #2c3e50; color: white; width: 100%;
        border-radius: 10px; padding: 10px; margin-top: 10px;
    }
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
                <button class="btn btn-cart">Add to Cart</button>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}
"""
# Ensure directory exists
if not os.path.exists(templates_dir):
    os.makedirs(templates_dir)

# Overwrite home.html
with open(os.path.join(templates_dir, 'home.html'), 'w', encoding='utf-8') as f:
    f.write(home_html_content)
print("✅ FIXED: home.html (Design updated & Error removed)")

print("-" * 30)
print("🚀 ALL SYSTEMS FIXED! Now Restart Server.")
print("-" * 30)