import os
import time

# 1. Path Setup
base_dir = os.getcwd()
target_file = os.path.join(base_dir, 'store', 'templates', 'store', 'home.html')

print(f"🎯 Target File: {target_file}")

# 2. DELETE Existing File (To break OneDrive lock)
if os.path.exists(target_file):
    try:
        os.remove(target_file)
        print("🗑️ Old file DELETED successfully.")
        time.sleep(1) # Wait for Windows to register deletion
    except Exception as e:
        print(f"⚠️ Could not delete file: {e}")

# 3. CREATE Fresh Content (NO floatform error)
html_content = """{% extends 'store/base.html' %}
{% block content %}
<style>
    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(to right, #2c3e50, #4ca1af);
        color: white;
        border-radius: 20px;
        padding: 40px;
        margin-bottom: 40px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .product-card {
        border: none;
        background: white;
        border-radius: 15px;
        overflow: hidden;
        transition: transform 0.3s, box-shadow 0.3s;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        height: 100%;
    }
    .product-card:hover { transform: translateY(-5px); box-shadow: 0 15px 30px rgba(0,0,0,0.15); }
    .product-img-container { position: relative; height: 250px; background: #f4f4f4; display: flex; align-items: center; justify-content: center; }
    .product-img { max-height: 200px; max-width: 90%; object-fit: contain; }
    .card-body { padding: 20px; }
    .badge-offer { position: absolute; top: 10px; right: 10px; background: #e74c3c; color: white; padding: 5px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }
    .product-title { font-weight: 600; font-size: 16px; color: #2c3e50; margin-bottom: 5px; }
    .price { font-size: 18px; font-weight: bold; color: #2c3e50; }
    .old-price { font-size: 14px; text-decoration: line-through; color: #95a5a6; margin-left: 5px; }
    .btn-cart { background-color: #2c3e50; color: white; width: 100%; border-radius: 10px; padding: 10px; font-weight: 500; transition: background 0.3s; }
    .btn-cart:hover { background-color: #e74c3c; color: white; }
</style>

<div class="hero-banner">
    <h1>Welcome to Trendflix</h1>
    <p>Discover the latest trends in fashion.</p>
</div>

<h3 class="mb-4" style="font-weight: 600; color: #2c3e50;">Latest Arrivals</h3>

<div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4">
    {% for product in products %}
    <div class="col">
        <div class="product-card">
            <div class="product-img-container">
                <span class="badge-offer">HOT</span>
                <img src="{{ product.image_url }}" class="product-img" alt="{{ product.name }}">
            </div>
            <div class="card-body">
                <h5 class="product-title text-truncate">{{ product.name }}</h5>
                <div class="d-flex align-items-center mb-3">
                    <span class="price">₹{{ product.selling_price }}</span>
                    <span class="old-price">₹{{ product.original_price }}</span>
                </div>
                <button class="btn btn-cart">Add to Cart</button>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}
"""

# Write New File
with open(target_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ New file WRITTEN successfully.")

# 4. VERIFICATION (Romba Mukkiyam)
with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()
    if "floatform" in content:
        print("❌ FAILURE: 'floatform' is STILL inside the file!")
    else:
        print("🚀 SUCCESS: File is CLEAN. No 'floatform' error found.")
        print("👉 Now start your server.")