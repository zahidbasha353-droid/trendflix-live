import requests
from bs4 import BeautifulSoup
import random

# Fake User Agents (Amazon Block pannama irukka)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
]

def get_amazon_details(url):
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return None
            
        soup = BeautifulSoup(response.content, "lxml")
        
        # 1. Get Title
        title_tag = soup.find("span", attrs={"id": "productTitle"})
        title = title_tag.get_text().strip() if title_tag else "New Amazon Product"
        
        # 2. Get Price
        price = 0
        price_tag = soup.find("span", attrs={"class": "a-price-whole"})
        if not price_tag:
            price_tag = soup.find("span", attrs={"class": "a-offscreen"})
            
        if price_tag:
            price_text = price_tag.get_text().replace(".", "").replace(",", "").replace("₹", "").strip()
            clean_price = ""
            for char in price_text:
                if char.isdigit():
                    clean_price += char
            if clean_price:
                price = int(clean_price)
            
        # 3. Get Image
        image_tag = soup.find("img", attrs={"id": "landingImage"})
        image_url = image_tag['src'] if image_tag else None
        
        return {
            "name": title,
            "price": price,
            "image_url": image_url
        }
        
    except Exception as e:
        print(f"Error scraping: {e}")
        return None