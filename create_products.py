import os
import django

# Django செட்டிங்ஸை இணைக்கிறோம்
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trendflix_core.settings')
django.setup()

from store.models import Product, Category
from django.core.files.base import ContentFile
import requests

def create_dummy_products():
    # 1. T-Shirts கேட்டகிரி உருவாக்குகிறோம்
    category, created = Category.objects.get_or_create(name='T-Shirts', slug='t-shirts')
    print(f"📂 Category: {category.name}")
    
    # 2. 10 சூப்பர் ப்ராடக்ட்ஸ் பட்டியல்
    products_data = [
        {'name': 'Urban Cool Tee', 'price': 499, 'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=600&q=80'},
        {'name': 'Vintage Vibe Shirt', 'price': 599, 'image': 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=600&q=80'},
        {'name': 'Streetwear Hoodie', 'price': 999, 'image': 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=600&q=80'},
        {'name': 'Graphic Print Tee', 'price': 450, 'image': 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=600&q=80'},
        {'name': 'Classic White Polo', 'price': 699, 'image': 'https://images.unsplash.com/photo-1586363104862-3a5e2ab60d99?w=600&q=80'},
        {'name': 'Oversized Fit Tee', 'price': 550, 'image': 'https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=600&q=80'},
        {'name': 'Striped Casual Shirt', 'price': 799, 'image': 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=600&q=80'},
        {'name': 'Denim Jacket', 'price': 1299, 'image': 'https://images.unsplash.com/photo-1576871337622-98d48d1cf531?w=600&q=80'},
        {'name': 'Summer Floral Shirt', 'price': 650, 'image': 'https://images.unsplash.com/photo-1598033129183-c4f50c736f10?w=600&q=80'},
        {'name': 'Basic Black Tee', 'price': 399, 'image': 'https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=600&q=80'},
    ]

    print("🚀 Starting to create products...")
    for i, data in enumerate(products_data):
        # ஏற்கனவே இந்த ப்ராடக்ட் இருக்கான்னு செக் பண்றோம் (டூப்ளிகேட் ஆகாம இருக்க)
        if not Product.objects.filter(name=data['name']).exists():
            try:
                # படத்தை டவுன்லோட் செய்கிறோம்
                response = requests.get(data['image'])
                if response.status_code == 200:
                    product = Product.objects.create(
                        name=data['name'],
                        slug=data['name'].lower().replace(' ', '-'),
                        description="Premium quality fabric. Perfect for daily wear. 100% Cotton.",
                        price=data['price'],
                        category=category,
                        is_active=True
                    )
                    # படத்தை சேமிக்கிறோம்
                    product.image.save(f"new_prod_{i}.jpg", ContentFile(response.content), save=True)
                    print(f"✅ Created: {product.name}")
            except Exception as e:
                print(f"❌ Error on {data['name']}: {e}")
        else:
            print(f"⚠️ Skipped (Already exists): {data['name']}")

    print("\n🎉 All Done! Products are ready.")

if __name__ == '__main__':
    create_dummy_products()