import os

# PATHS
base_dir = os.getcwd()
templates_dir = os.path.join(base_dir, 'store', 'templates', 'store')

print("-" * 40)
print("🚀 UPGRADING UI: SLIDING BANNER + FULL WIDTH (NO GAPS)...")
print("-" * 40)

# ---------------------------------------------------------
# 1. UPDATE BASE.HTML (Force Full Width)
# ---------------------------------------------------------
base_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trendflix | Premium POD Store</title>
    
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        :root { 
            --primary-bg: #f8f9fa;
            --accent-color: #000;
        }
        body { 
            background-color: var(--primary-bg); 
            font-family: 'Poppins', sans-serif; 
            overflow-x: hidden; /* Prevent horizontal scroll */
        }
        
        /* Full Width Navbar */
        .navbar { background: white; padding: 15px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
        .navbar-brand { font-weight: 800; font-size: 26px; letter-spacing: -1px; }
        .nav-link { font-weight: 500; margin-left: 20px; color: #333 !important; }
        .search-box { border-radius: 50px 0 0 50px; background: #f1f1f1; border: none; padding-left: 20px; }
        .search-btn { border-radius: 0 50px 50px 0; background: #000; color: white; border: none; padding: 0 25px; }
        .cart-badge { background-color: #e11d48; color: white; font-size: 11px; }

        /* Footer */
        footer { background: #111; color: #aaa; padding: 50px 0; margin-top: 50px; text-align: center; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg sticky-top">
        <div class="container-fluid px-4"> <a class="navbar-brand" href="/"><i class="fa-solid fa-shirt text-danger"></i> TRENDFLIX</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"><span class="navbar-toggler-icon"></span></button>
            
            <div class="collapse navbar-collapse" id="navbarNav">
                <form class="d-flex mx-auto" style="width: 50%;">
                    <input class="form-control search-box" type="search" placeholder="Search T-Shirts, Hoodies...">
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
            <h3>Trendflix</h3>
            <p>India's #1 Premium Print-on-Demand Store</p>
            <p>&copy; 2025 Trendflix. All rights reserved.</p>
        </div>
    </footer>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
with open(os.path.join(templates_dir, 'base.html'), 'w', encoding='utf-8') as f:
    f.write(base_html)
print("✅ Base Layout Updated (Full Screen Mode).")

# ---------------------------------------------------------
# 2. UPDATE HOME.HTML (Sliding Banner + Tight Grid)
# ---------------------------------------------------------
home_html = """{% extends 'store/base.html' %}

{% block content %}
<style>
    /* Carousel / Sliding Banner */
    .carousel-item {
        height: 500px; /* Big Banner Height */
    }
    .carousel-item img {
        object-fit: cover;
        height: 100%;
        width: 100%;
        filter: brightness(0.7); /* Darken image slightly for text readability */
    }
    .carousel-caption {
        bottom: 40%;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.8);
    }
    .carousel-caption h1 { font-size: 4rem; font-weight: 800; }
    .btn-hero { background: white; color: black; padding: 12px 30px; font-weight: 700; border-radius: 30px; text-decoration: none; margin-top: 10px; display: inline-block; }
    .btn-hero:hover { background: #f1f1f1; transform: scale(1.05); transition: 0.3s; }

    /* Product Grid - Full Width & Tight */
    .product-grid-wrapper {
        padding: 30px;
        background: white;
    }
    
    .product-card {
        border: 1px solid #eee;
        transition: 0.3s;
        height: 100%;
        padding: 10px;
        border-radius: 8px;
        background: white;
    }
    .product-card:hover { border-color: #333; transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
    
    .img-wrap {
        height: 250px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        margin-bottom: 10px;
    }
    .img-wrap img { max-height: 100%; max-width: 100%; object-fit: contain; }
    
    .p-title { font-weight: 600; font-size: 15px; margin-bottom: 5px; color: #333; }
    .p-price { font-weight: 700; color: #e11d48; font-size: 17px; }
    
    .btn-cart-sm { width: 100%; background: #111; color: white; border: none; padding: 8px; border-radius: 5px; font-size: 13px; font-weight: 500; }
    .btn-cart-sm:hover { background: #333; }
</style>

<div id="heroCarousel" class="carousel slide" data-bs-ride="carousel">
    <div class="carousel-indicators">
        <button type="button" data-bs-target="#heroCarousel" data-bs-slide-to="0" class="active"></button>
        <button type="button" data-bs-target="#heroCarousel" data-bs-slide-to="1"></button>
        <button type="button" data-bs-target="#heroCarousel" data-bs-slide-to="2"></button>
    </div>
    
    <div class="carousel-inner">
        <div class="carousel-item active">
            <img src="https://images.unsplash.com/photo-1523381210434-271e8be1f52b?q=80&w=2070&auto=format&fit=crop" class="d-block w-100" alt="Fashion 1">
            <div class="carousel-caption d-none d-md-block">
                <h1>Print Your Style</h1>
                <p class="lead">Premium Custom T-Shirts & Hoodies</p>
                <a href="#collection" class="btn-hero">Shop Now</a>
            </div>
        </div>
        <div class="carousel-item">
            <img src="https://images.unsplash.com/photo-1483985988355-763728e1935b?q=80&w=2070&auto=format&fit=crop" class="d-block w-100" alt="Fashion 2">
            <div class="carousel-caption d-none d-md-block">
                <h1>New Arrivals</h1>
                <p class="lead">Trending Designs for 2025</p>
                <a href="#collection" class="btn-hero">Explore</a>
            </div>
        </div>
        <div class="carousel-item">
            <img src="https://images.unsplash.com/photo-1441984904996-e0b6ba687e04?q=80&w=2070&auto=format&fit=crop" class="d-block w-100" alt="Fashion 3">
            <div class="carousel-caption d-none d-md-block">
                <h1>Flat 50% Off</h1>
                <p class="lead">On All Winter Collections</p>
                <a href="#collection" class="btn-hero">Grab Deal</a>
            </div>
        </div>
    </div>
    
    <button class="carousel-control-prev" type="button" data-bs-target="#heroCarousel" data-bs-slide="prev">
        <span class="carousel-control-prev-icon"></span>
    </button>
    <button class="carousel-control-next" type="button" data-bs-target="#heroCarousel" data-bs-slide="next">
        <span class="carousel-control-next-icon"></span>
    </button>
</div>

<div class="product-grid-wrapper" id="collection">
    <h3 class="mb-4 fw-bold text-center">Trending Collections</h3>
    
    <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 row-cols-xl-5 g-3">
        {% for product in products %}
        <div class="col">
            <div class="product-card">
                <a href="{% url 'product_detail' product.id %}" style="text-decoration: none; color: inherit;">
                    <div class="img-wrap">
                        <img src="{{ product.image_url }}" alt="{{ product.name }}">
                    </div>
                    <div class="p-title text-truncate">{{ product.name }}</div>
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <span class="p-price">₹{{ product.selling_price }}</span>
                        <small class="text-muted text-decoration-line-through">₹{{ product.original_price }}</small>
                    </div>
                </a>
                <div class="d-grid gap-2">
                     <a href="{% url 'buy_now' product.id %}" class="btn-cart-sm bg-warning text-dark border-0">Buy Now</a>
                     <a href="{% url 'add_to_cart' product.id %}" class="btn-cart-sm">Add to Cart</a>
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
print("✅ Home Page Updated (Sliding Banner & No-Gap Grid).")

print("-" * 40)
print("🚀 UI TRANSFORMATION COMPLETE!")
print("Run 'python manage.py runserver' and refresh.")
print("-" * 40)