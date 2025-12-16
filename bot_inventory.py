import os
import django
import random

# 1. SETUP DJANGO ENVIRONMENT
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trendflix_core.settings')
django.setup()

from store.models import Product

# 2. PRODUCT DATA (Sample Dropshipping Products)
products_list = [
    {
        "name": "Men's Premium Cotton T-Shirt (Black)",
        "price": 499,
        "original": 999,
        "image": "https://m.media-amazon.com/images/I/71-3+K+u3BL._AC_UY1100_.jpg",
        "category": "Fashion"
    },
    {
        "name": "Smart Watch Series 7 - Black",
        "price": 2499,
        "original": 5999,
        "image": "https://m.media-amazon.com/images/I/71sxlhYhKWL._AC_UY1100_.jpg",
        "category": "Electronics"
    },
    {
        "name": "Running Sneakers - Sporty White",
        "price": 1299,
        "original": 2999,
        "image": "https://m.media-amazon.com/images/I/71oEKkghg-L._AC_UY1000_.jpg",
        "category": "Footwear"
    },
    {
        "name": "Wireless Noise Cancelling Headphones",
        "price": 1999,
        "original": 4999,
        "image": "https://m.media-amazon.com/images/I/51+i+b9uRIL._AC_UY1100_.jpg",
        "category": "Electronics"
    },
    {
        "name": "Classic Aviator Sunglasses",
        "price": 799,
        "original": 1499,
        "image": "https://m.media-amazon.com/images/I/51Ui-l+3+LL._AC_UY1100_.jpg",
        "category": "Accessories"
    },
    {
        "name": "Denim Jacket - Vintage Blue",
        "price": 1499,
        "original": 3499,
        "image": "https://m.media-amazon.com/images/I/81x1+N7yZ4L._AC_UY1100_.jpg",
        "category": "Fashion"
    },
    {
        "name": "Gaming Mouse RGB",
        "price": 899,
        "original": 1999,
        "image": "https://m.media-amazon.com/images/I/61mpMH5TzkL._AC_UY1000_.jpg",
        "category": "Electronics"
    },
    {
        "name": "Leather Wallet for Men",
        "price": 599,
        "original": 1299,
        "image": "https://m.media-amazon.com/images/I/81Mc+V-9WJL._AC_UY1100_.jpg",
        "category": "Accessories"
    },
    {
        "name": "4K Action Camera Waterproof",
        "price": 3999,
        "original": 8999,
        "image": "https://m.media-amazon.com/images/I/71kv0B3WgnL._AC_UY1100_.jpg",
        "category": "Electronics"
    },
    {
        "name": "Stainless Steel Water Bottle",
        "price": 399,
        "original": 999,
        "image": "https://m.media-amazon.com/images/I/61j6oyP3dDL._AC_UY1100_.jpg",
        "category": "Home"
    }
]

print("-" * 40)
print("🤖 BOT STARTED: Adding Products to Inventory...")
print("-" * 40)

# 3. LOOP & ADD PRODUCTS
count = 0
for item in products_list:
    # Check if product already exists (to avoid duplicates)
    if not Product.objects.filter(name=item['name']).exists():
        Product.objects.create(
            name=item['name'],
            description=f"High quality {item['category']} product. Best seller in 2025.",
            original_price=item['original'],
            selling_price=item['price'],
            image_url=item['image'],
            sku=f"SKU-{random.randint(1000, 9999)}",
            rating=random.uniform(4.0, 5.0),
            reviews_count=random.randint(50, 500),
            is_bestseller=random.choice([True, False])
        )
        print(f"✅ Added: {item['name']}")
        count += 1
    else:
        print(f"⚠️ Skipped: {item['name']} (Already exists)")

print("-" * 40)
print(f"🚀 SUCCESS! Bot added {count} new products.")
print("👉 Refresh your website to see the magic!")
print("-" * 40)