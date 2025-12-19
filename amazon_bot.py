import os
import django
import requests
from bs4 import BeautifulSoup
import time

# Django settings-ah load panna
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trendflix_core.settings')
django.setup()

from store.models import Product, Category

def start_bulk_automation(search_url, category_id):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "en-US, en;q=0.5"
    }
    
    print(f"🔄 Amazon-la products theduram... Category ID: {category_id}")
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Amazon search results-la irukra ella product cards-ayum edukkirom
    items = soup.find_all("div", {"data-component-type": "s-search-result"})
    cat = Category.objects.get(id=category_id)

    for item in items:
        try:
            # 1. Title
            title = item.h2.text.strip()
            
            # 2. Price
            price_span = item.find("span", "a-price-whole")
            price = float(price_span.text.replace(',', '')) if price_span else 0.0
            
            # 3. Rating
            rating_tag = item.find("span", "a-icon-alt")
            rating = rating_tag.text.split()[0] if rating_tag else "4.0"
            
            # 4. Image
            img_tag = item.find("img", "s-image")
            image_url = img_tag['src'] if img_tag else ""

            # 5. Link + Affiliate ID
            link_tag = item.find("a", "a-link-normal")
            raw_url = "https://www.amazon.in" + link_tag['href']
            affiliate_url = f"{raw_url.split('?')[0]}?tag=zahidbasha-21" # Zahidbasha-21 ID auto-add aagum

            # Database-la add pannurom
            p, created = Product.objects.get_or_create(
                name=title[:200],
                category=cat,
                defaults={
                    'selling_price': price,
                    'cost_price': price + 200,
                    'image_url_path': image_url,
                    'affiliate_link': affiliate_url,
                    'rating': rating,
                    'is_approved': True
                }
            )
            
            if created:
                print(f"✅ Success: {title[:30]}... Added!")
            else:
                print(f"⏭️ Already exists: {title[:30]}")
                
            time.sleep(2) # Amazon block pannaama irukka gap

        except Exception as e:
            continue

# --- RUN IT ---
# Example: Amazon search URL and Category ID (Admin-la categories ponga, ID theriyum)
search_url = "https://www.amazon.in/s?k=mens+tshirt" 
start_bulk_automation(search_url, category_id=1)