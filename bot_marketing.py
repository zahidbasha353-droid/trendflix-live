import os
import django
import random

# 1. SETUP DJANGO ENVIRONMENT
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trendflix_core.settings')
django.setup()

from store.models import Product

# 2. MARKETING TEMPLATES (Catchy Captions)
captions_styles = [
    "🔥 FLASH SALE ALERT! 🔥\nGet the {name} for just ₹{price}!\nLimited stock available. Order now before it's gone! 🚀",
    
    "✨ New Arrival ✨\nUpgrade your style with {name}.\nPremium quality, best price: ₹{price} (Was ₹{original}).\nShop Link in Bio! 🛍️",
    
    "😍 Must Have Product!\nEveryone is talking about the {name}.\nGrab yours today for only ₹{price}.\nDon't miss out! 💯",
    
    "🎁 Perfect Gift Idea 🎁\nLooking for something special? check out {name}.\nNow available at Trendflix for ₹{price}.\nFast Delivery! 🚚"
]

hashtags_list = "#Trendflix #OnlineShopping #Deals #Fashion #Tech #Style #IndiaShopping #Offer #Discount"

print("-" * 40)
print("🤖 MARKETING BOT: Generating Instagram Post...")
print("-" * 40)

# 3. PICK RANDOM PRODUCT
products = list(Product.objects.all())

if not products:
    print("❌ No products found!")
else:
    # Pick one lucky product
    product = random.choice(products)
    
    # Pick a random caption style
    template = random.choice(captions_styles)
    
    # Fill in the details
    final_caption = template.format(
        name=product.name,
        price=product.selling_price,
        original=product.original_price
    )

    # 4. PRINT THE POST (Ready for Instagram)
    print("\n📱 --- INSTAGRAM POST PREVIEW --- 📱\n")
    print(f"🖼️ IMAGE: {product.image_url}")
    print("\n📝 CAPTION:")
    print(final_caption)
    print(f"\n🏷️ HASHTAGS:\n{hashtags_list}")
    print("\n------------------------------------")
    print(f"👉 Copy this image & text to Instagram!")