import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_to_csv(search_url, category_id):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    }
    
    print(f"🔍 Amazon-la products theduram... Category ID: {category_id}")
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    items = soup.find_all("div", {"data-component-type": "s-search-result"})

    # CSV File-ah local-la save pannuvom
    with open('products_upload.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'selling_price', 'cost_price', 'image_url_path', 'affiliate_link', 'rating', 'category_id'])

        for item in items[:15]:
            try:
                title = item.h2.text.strip()
                price_span = item.find("span", "a-price-whole")
                price = price_span.text.replace(',', '').strip() if price_span else "0"
                
                rating_tag = item.find("span", {"class": "a-icon-alt"})
                rating = rating_tag.text.split()[0] if rating_tag else "4.2"
                img_tag = item.find("img", "s-image")
                image_url = img_tag['src'] if img_tag else ""

                link_tag = item.find("a", "a-link-normal")
                raw_url = "https://www.amazon.in" + link_tag['href']
                # Unga zahidbasha-21 ID sethu link create aagum
                affiliate_url = f"{raw_url.split('?')[0]}?tag=zahidbasha-21"

                writer.writerow([title[:200], price, float(price)+200, image_url, affiliate_url, rating, category_id])
                print(f"✅ Saved to CSV: {title[:30]}...")
            except Exception as e:
                continue

# Run locally to generate CSV
scrape_to_csv("https://www.amazon.in/s?k=mens+tshirt", category_id=1)
print("🏁 products_upload.csv ready! Ippo idhai PythonAnywhere-ku upload pannunga.")