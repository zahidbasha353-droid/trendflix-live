import os

# PATHS
base_dir = os.getcwd()
templates_dir = os.path.join(base_dir, 'store', 'templates', 'store')

print("-" * 40)
print("🎨 UPGRADING TO AMAZON STYLE (FULL WIDTH)...")
print("-" * 40)

# ---------------------------------------------------------
# 1. UPDATE BASE.HTML (Make it Full Width)
# ---------------------------------------------------------
base_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trendflix | Premium Store</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        :root { --primary-color: #131921; --accent-color: #febd69; --text-color: #333; }
        body { background-color: #eaeded; font-family: 'Inter', sans-serif; }
        
        /* Navbar (Amazon Style) */
        .navbar { background-color: var(--primary-color) !important; padding: 10px 0; color: white; }
        .navbar-brand { font-weight: 800; font-size: 24px; color: white !important; letter-spacing: -1px; }
        .nav-link { color: white !important; font-weight: 500; }
        .nav-link:hover { border: 1px solid white; border-radius: 2px; }
        
        /* Search Bar */
        .search-box { border-radius: 4px 0 0 4px; border: none; }
        .search-btn { background-color: var(--accent-color); border: none; border-radius: 0 4px 4px 0; }
        .search-btn:hover { background-color: #f3a847; }
        
        /* Cart Badge */
        .cart-badge { background-color: var(--accent-color); color: var(--primary-color); font-weight: bold; }
        
        footer { background-color: #232f3e; color: #ddd; padding: 40px 0; margin-top: 60px; text-align: center; font-size: 14px; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg sticky-top">
        <div class="container-fluid px-4"> <a class="navbar-brand" href="/"><i class="fa-solid fa-bag-shopping text-warning"></i> TRENDFLIX</a>
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

    <div class="container-fluid px-4 mt-4"> 
        {% block content %}{% endblock %}
    </div>

    <footer>
        <div class="container"><p>&copy; 2025 Trendflix. All rights reserved.</p></div>
    </footer>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
with open(os.path.join(templates_dir, 'base.html'), 'w', encoding='utf-8') as f:
    f.write(base_html)
print("✅ Navbar & Layout updated to Full Width.")

# ---------------------------------------------------------
# 2. UPDATE HOME.HTML (Big Banner & Better Grid)
# ---------------------------------------------------------
home_html = """{% extends 'store/base.html' %}

{% block content %}
<style>
    /* Hero Banner (Amazon Style) */
    .hero-banner {
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://images.unsplash.com/photo-1483985988355-763728e1935b?q=80&w=2070&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        height: 400px; /* Big Height */
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        text-align: center;
        margin: -1.5rem -1.5rem 30px -1.5rem; /* Stretch to edges */
    }
    
    .hero-content h1 { font-size: 3.5rem; font-weight: 800; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }
    .hero-content p { font-size: 1.2rem; margin-bottom: 20px; }
    
    /* Product Card */
    .product-card {
        background: white;
        border: 1px solid #ddd;
        border-radius: 0px; /* Amazon style is boxy */
        padding: 20px;
        height: 100%;
        transition: transform 0.2s;
    }
    .product-card:hover { transform: scale(1.02); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
    
    .product-img-container { height: 200px; display: flex; align-items: center; justify-content: center; margin-bottom: 15px; }
    .product-img { max-height: 100%; max-width: 100%; object-fit: contain; }
    
    .price { font-size: 20px; font-weight: 700; color: #B12704; } /* Amazon Price Color */
    .old-price { font-size: 14px; text-decoration: line-through; color: #565959; }
    
    .btn-cart {
        background-color: #ffd814; border: 1px solid #fcd200; color: #111;
        width: 100%; border-radius: 20px; padding: 8px; font-weight: 500; text-decoration: none; display: block; text-align: center;
    }
    .btn-cart:hover { background-color: #f7ca00; }
</style>

<div class="hero-banner">
    <div class="hero-content">
        <h1>Fashion Ends Here.</h1>
        <p>Up to 60% Off on Top Brands | Shop Now</p>
        <button class="btn btn-warning btn-lg px-5" style="border-radius: 30px; font-weight: bold;">Explore Deals</button>
    </div>
</div>

<div class="bg-white p-4" style="margin-top: -50px; position: relative; z-index: 10;">
    <h3 class="mb-4" style="font-weight: 700; border-bottom: 2px solid #eee; padding-bottom: 10px;">Recommended for You</h3>
    
    <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 row-cols-xl-5 g-3">
        {% for product in products %}
        <div class="col">
            <div class="product-card">
                <div class="product-img-container">
                    <img src="{{ product.image_url }}" class="product-img" alt="{{ product.name }}">
                </div>
                <div class="card-body p-0">
                    <h6 class="text-truncate mb-1" style="color: #007185; font-weight: 500;">{{ product.name }}</h6>
                    <div class="mb-2">
                        <i class="fa-solid fa-star text-warning small"></i>
                        <i class="fa-solid fa-star text-warning small"></i>
                        <i class="fa-solid fa-star text-warning small"></i>
                        <i class="fa-solid fa-star text-warning small"></i>
                        <i class="fa-solid fa-star-half-stroke text-warning small"></i>
                        <span class="text-primary small ms-1">{{ product.reviews_count }}</span>
                    </div>
                    <div class="mb-2">
                        <span class="price">₹{{ product.selling_price }}</span>
                        <span class="old-price ms-2">₹{{ product.original_price }}</span>
                    </div>
                    <a href="{% url 'add_to_cart' product.id %}" class="btn btn-cart">Add to Cart</a>
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
print("✅ Home Page updated with Big Banner & Pro Grid.")

print("-" * 40)
print("🚀 DESIGN UPGRADE COMPLETE! Refresh your website.")
print("-" * 40)