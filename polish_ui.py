import os

# PATHS
base_dir = os.getcwd()
templates_dir = os.path.join(base_dir, 'store', 'templates', 'store')

print("-" * 40)
print("✨ APPLYING 'FEEL GOOD' UI POLISH...")
print("-" * 40)

# ---------------------------------------------------------
# 1. UPDATE BASE.HTML (Fonts, Navbar, Footer - Premium Look)
# ---------------------------------------------------------
base_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trendflix | Premium Shopping</title>
    
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        :root { 
            --primary-bg: #f3f4f6;       /* Soft Gray Background */
            --card-bg: #ffffff;          /* Pure White */
            --text-main: #1f2937;        /* Dark Gray Text */
            --text-light: #6b7280;       /* Light Gray Text */
            --accent-color: #2563eb;     /* Professional Blue */
            --brand-yellow: #fbbf24;     /* Star Color */
            --nav-bg: #ffffff;
        }

        body { 
            background-color: var(--primary-bg); 
            font-family: 'Poppins', sans-serif; 
            color: var(--text-main);
            overflow-x: hidden;
        }
        
        /* Navbar Styling */
        .navbar { 
            background-color: var(--nav-bg) !important; 
            padding: 15px 0; 
            box-shadow: 0 4px 20px rgba(0,0,0,0.05); /* Soft Shadow */
        }
        .navbar-brand { 
            font-weight: 700; 
            font-size: 26px; 
            color: #111 !important; 
            letter-spacing: -0.5px; 
        }
        .nav-link { 
            color: #4b5563 !important; 
            font-weight: 500; 
            margin-left: 20px; 
            transition: 0.3s;
        }
        .nav-link:hover { color: var(--accent-color) !important; transform: translateY(-2px); }
        
        /* Search Bar */
        .search-box { 
            border-radius: 50px 0 0 50px; 
            border: 1px solid #e5e7eb; 
            padding-left: 20px;
            background: #f9fafb;
        }
        .search-btn { 
            background-color: #111; 
            color: white;
            border: none; 
            border-radius: 0 50px 50px 0; 
            padding: 0 25px;
            transition: 0.3s;
        }
        .search-btn:hover { background-color: #333; }
        
        /* Cart Badge */
        .cart-badge { 
            background-color: #ef4444; 
            color: white; 
            font-size: 11px;
        }
        
        /* Footer */
        footer { 
            background-color: #111; 
            color: #9ca3af; 
            padding: 60px 0; 
            margin-top: 80px; 
            text-align: center; 
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg sticky-top">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fa-solid fa-bag-shopping text-danger"></i> TRENDFLIX
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"><span class="navbar-toggler-icon"></span></button>
            
            <div class="collapse navbar-collapse" id="navbarNav">
                <form class="d-flex mx-auto" style="width: 50%;">
                    <input class="form-control search-box" type="search" placeholder="Search for products...">
                    <button class="btn search-btn" type="submit"><i class="fa-solid fa-magnifying-glass"></i></button>
                </form>
                
                <ul class="navbar-nav ms-auto align-items-center">
                    {% if user.is_authenticated %}
                        <li class="nav-item"><a href="#" class="nav-link">Hi, {{ user.username }}</a></li>
                        <li class="nav-item"><a href="{% url 'logout' %}" class="nav-link text-danger">Logout</a></li>
                    {% else %}
                        <li class="nav-item"><a href="{% url 'login' %}" class="nav-link">Login</a></li>
                    {% endif %}
                    <li class="nav-item">
                        <a href="{% url 'cart' %}" class="nav-link position-relative">
                            <i class="fa-solid fa-cart-shopping fa-lg"></i>
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

    <footer>
        <div class="container">
            <h5 class="text-white mb-3">Trendflix</h5>
            <p>Premium Fashion & Lifestyle Store</p>
            <p>&copy; 2025 Trendflix. All rights reserved.</p>
        </div>
    </footer>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
with open(os.path.join(templates_dir, 'base.html'), 'w', encoding='utf-8') as f:
    f.write(base_html)
print("✅ Base Template Updated (Modern Fonts & Colors).")

# ---------------------------------------------------------
# 2. UPDATE HOME.HTML (Premium Cards & Hover Effects)
# ---------------------------------------------------------
home_html = """{% extends 'store/base.html' %}

{% block content %}
<style>
    /* Hero Section */
    .hero-banner {
        background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), url('https://images.unsplash.com/photo-1483985988355-763728e1935b?q=80&w=2070&auto=format&fit=crop');
        background-size: cover; 
        background-position: center;
        height: 450px; 
        display: flex; 
        align-items: center; 
        justify-content: center;
        width: 100%; 
        color: white;
        text-align: center;
        border-radius: 0 0 50px 50px; /* Modern curve */
        margin-bottom: 50px;
    }
    
    .hero-content h1 { font-size: 4rem; font-weight: 700; text-shadow: 0 10px 30px rgba(0,0,0,0.3); }
    .hero-btn { 
        background: white; color: #111; 
        padding: 12px 35px; border-radius: 30px; 
        font-weight: 600; text-decoration: none; 
        transition: 0.3s;
    }
    .hero-btn:hover { background: #f3f4f6; transform: scale(1.05); }
    
    /* Product Grid */
    .section-title { font-weight: 700; color: #111; margin-bottom: 30px; text-align: center; font-size: 2rem; }
    
    /* Premium Product Card */
    .product-card {
        background: white;
        border: none;
        border-radius: 20px;
        padding: 15px;
        transition: all 0.3s ease;
        position: relative;
        height: 100%;
        box-shadow: 0 10px 30px rgba(0,0,0,0.03); /* Very subtle shadow */
    }
    
    .product-card:hover { 
        transform: translateY(-10px); 
        box-shadow: 0 20px 40px rgba(0,0,0,0.1); 
    }
    
    .product-link { text-decoration: none; color: inherit; }
    
    .product-img-container {
        height: 220px;
        background: #f8f9fa;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 15px;
        overflow: hidden;
    }
    
    .product-img { max-height: 160px; transition: 0.3s; }
    .product-card:hover .product-img { transform: scale(1.1); }
    
    .product-title { font-weight: 600; font-size: 16px; margin-bottom: 5px; color: #1f2937; }
    .stars { color: #fbbf24; font-size: 14px; }
    
    .price-row { display: flex; align-items: center; justify-content: space-between; margin-top: 10px; }
    .price { font-size: 18px; font-weight: 700; color: #111; }
    .old-price { font-size: 13px; text-decoration: line-through; color: #9ca3af; }
    
    /* Buttons */
    .btn-action {
        border-radius: 12px;
        padding: 8px 0;
        font-weight: 500;
        font-size: 14px;
        text-align: center;
        text-decoration: none;
        display: block;
        transition: 0.2s;
        width: 48%;
    }
    
    .btn-add { background-color: #f3f4f6; color: #111; }
    .btn-add:hover { background-color: #e5e7eb; }
    
    .btn-buy { background-color: #111; color: white; }
    .btn-buy:hover { background-color: #333; box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
</style>

<div class="hero-banner">
    <div class="hero-content">
        <h1>Summer Collection</h1>
        <p class="mb-4 text-white-50">Discover the trendiest styles of 2025.</p>
        <a href="#shop" class="hero-btn">Explore Now</a>
    </div>
</div>

<div class="container mb-5" id="shop">
    <h3 class="section-title">Trending Now</h3>
    
    <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4">
        {% for product in products %}
        <div class="col">
            <div class="product-card">
                <a href="{% url 'product_detail' product.id %}" class="product-link">
                    <div class="product-img-container">
                        <img src="{{ product.image_url }}" class="product-img" alt="{{ product.name }}">
                    </div>
                    
                    <div class="px-2">
                        <h6 class="product-title text-truncate">{{ product.name }}</h6>
                        <div class="stars">
                            <i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star-half-stroke"></i>
                            <span class="text-muted ms-1 small">({{ product.reviews_count }})</span>
                        </div>
                        
                        <div class="price-row">
                            <div>
                                <span class="price">₹{{ product.selling_price }}</span>
                                <span class="old-price ms-1">₹{{ product.original_price }}</span>
                            </div>
                        </div>
                    </div>
                </a>
                
                <div class="d-flex justify-content-between mt-3 px-2">
                    <a href="{% url 'add_to_cart' product.id %}" class="btn-action btn-add">Add</a>
                    <a href="{% url 'buy_now' product.id %}" class="btn-action btn-buy">Buy Now</a>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}
"""
with open(os.path.join(templates_dir, 'home.html'), 'w', encoding='utf-8') as f:
    f.write(home_html)
print("✅ Home Page Polished (Floating Cards & Smooth Buttons).")

print("-" * 40)
print("🚀 UI POLISHED! Refresh your website now.")
print("-" * 40)