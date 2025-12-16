import requests
import json

# --- 🔐 FILL THESE DETAILS ---
API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzN2Q0YmQzMDM1ZmUxMWU5YTgwM2FiN2VlYjNjY2M5NyIsImp0aSI6ImI1NDM5Y2IzZjIyODUwOGQwMTk3NzUyYjYzOTIxNjI1NTNkZDMxMDQ1NGQxYWYxYWY2M2Q1ZTAwNmE3ZGFmYzQ3MGNmZjJjNTY2ODQzMjE3IiwiaWF0IjoxNzY1ODE5NDkwLjgyNjQ1NywibmJmIjoxNzY1ODE5NDkwLjgyNjQ1OCwiZXhwIjoxNzk3MzU1NDkwLjgxNjg1LCJzdWIiOiIyNTcxNjE3NyIsInNjb3BlcyI6WyJzaG9wcy5tYW5hZ2UiLCJzaG9wcy5yZWFkIiwiY2F0YWxvZy5yZWFkIiwib3JkZXJzLnJlYWQiLCJvcmRlcnMud3JpdGUiLCJwcm9kdWN0cy5yZWFkIiwicHJvZHVjdHMud3JpdGUiLCJ3ZWJob29rcy5yZWFkIiwid2ViaG9va3Mud3JpdGUiLCJ1cGxvYWRzLnJlYWQiLCJ1cGxvYWRzLndyaXRlIiwicHJpbnRfcHJvdmlkZXJzLnJlYWQiLCJ1c2VyLmluZm8iXX0.NYuRkmACFJI7dpxILoDjdj5-vrfId86sam5b2S5_l6fq9f54rt0vBQbZ75wzsO0vBX6VqhaE0cv-4J7yTMaDcvTtJeMRSJGuNTsA4_Nk6e6JXVn2ew0AZVm6Cpz1b7rkrrLXpL1FkNaIvWNNnEcj6lsTX_O_utDCZ0c3eyxltOjOZ-v6_vIKtSzu6zD_EQmKc9SwPArJ0ZyNMuwrIaPV2QszZ-d9s0CZGGD6hEfcvXoG2KcWjil-UGTTwZyjpDldY6mTr3FDJbjh2rHkCrCkayzaNDtbpQ-CNTiqR4QFhN2Jv3Rj-wI3Nvp1Jfue0zm491ZD6CPzNVGKCEJQ-0zGvX5khNFsfUQuTbI5pOI_BTRR4I9MFhgfqnNEaJmTMAaA0YE-NhUzYFBJAsIsZFhTuGGynjpXuur0WLcJSJuJFKELbgFCO8NK9XDkwA4Xc0c0k6DMusG59u5UPLogmSJHEI-H4JjY-Aut8ob4FNcPZMN2tLuq_GH2MSeqFk1X7o_w9YVIYCVoNxUgsN9cte2TmCBxiI8h6F0QfG4FiGNT1CH2W-HBCkaoCbN2QHn7yDp0e2W1yNOdefWF7hVN0ehugwygFbqpqdWObeLEkl6xStjk2V_JYoh5w4WpHZiHbYHXj4ccFTMl4umdEcv8WzCLVlHtvivtZfJUG9gmbWU34"
SHOP_ID = "25702412" 
# (Shop ID theriyalana paravalla, API Key mattum podunga, nan kandupidichu tharen)

def scan_printify():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    # 1. CHECK SHOPS (Shop ID confirm panna)
    print("\n🔍 Scanning for Shops...")
    shop_resp = requests.get("https://api.printify.com/v1/shops.json", headers=headers)
    
    if shop_resp.status_code == 200:
        shops = shop_resp.json()
        print(f"✅ Found {len(shops)} Shop(s):")
        for shop in shops:
            print(f"   🏠 Shop Name: {shop['title']}")
            print(f"   🔑 Shop ID:   {shop['id']}")  # <--- ITHU THAN UNMAIYANA SHOP ID
            print("-" * 30)
            
            # 2. CHECK PRODUCTS IN THIS SHOP
            print(f"   📦 Scanning Products in Shop {shop['id']}...")
            prod_resp = requests.get(f"https://api.printify.com/v1/shops/{shop['id']}/products.json", headers=headers)
            
            if prod_resp.status_code == 200:
                products = prod_resp.json().get('data', [])
                if not products:
                    print("      ⚠️ No products found here.")
                for p in products:
                    print(f"      👕 Product: {p['title']}")
                    print(f"      🔑 ID:      {p['id']}") # <--- ITHU THAN UNMAIYANA PRODUCT ID
                    print("      " + "."*20)
            else:
                print("      ❌ Could not fetch products.")
    else:
        print(f"❌ API Key Error! Status: {shop_resp.status_code}")
        print("Response:", shop_resp.text)

if __name__ == "__main__":
    scan_printify()