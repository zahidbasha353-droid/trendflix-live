import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trendflix_core.settings')
django.setup()

from store.models import Product

print("🧹 CLEARING OLD ELECTRONICS STOCK...")
Product.objects.all().delete()

print("👕 STOCKING UP PREMIUM CLOTHING...")

clothing_stock = [
    {"name": "Streetwear Oversized Tee (Black)", "price": 799, "img": "https://m.media-amazon.com/images/I/61S0+hF+g+L._AC_UY1100_.jpg"},
    {"name": "Classic White Polo T-Shirt", "price": 699, "img": "https://m.media-amazon.com/images/I/51p4L1uiIWL._AC_UY1100_.jpg"},
    {"name": "Urban Hoodie (Grey)", "price": 1499, "img": "https://m.media-amazon.com/images/I/51+i+b9uRIL._AC_UY1100_.jpg"},
    {"name": "Graphic Print Anime Tee", "price": 599, "img": "https://m.media-amazon.com/images/I/71wF7-sL3IL._AC_UY1100_.jpg"},
    {"name": "Sports Jersey - Blue", "price": 499, "img": "https://m.media-amazon.com/images/I/51j1-a+XqWL._AC_UY1100_.jpg"},
    {"name": "Premium Cotton V-Neck", "price": 899, "img": "https://m.media-amazon.com/images/I/81x1+N7yZ4L._AC_UY1100_.jpg"},
    {"name": "Couple Combo T-Shirts", "price": 1299, "img": "https://m.media-amazon.com/images/I/71E7Gg92fCL._AC_UY1100_.jpg"},
    {"name": "Full Sleeve Winter Tee", "price": 999, "img": "https://m.media-amazon.com/images/I/61-jBuhtgZL._AC_UY1100_.jpg"},
]

for item in clothing_stock:
    Product.objects.create(
        name=item['name'],
        description="Premium quality fabric. 100% Cotton. Breathable and comfortable fit.",
        original_price=item['price'] + 400,
        selling_price=item['price'],
        image_url=item['img'],
        sku=f"CLOTH-{random.randint(1000,9999)}",
        is_bestseller=True
    )

print("✅ STORE IS NOW 100% CLOTHING & POD READY!")