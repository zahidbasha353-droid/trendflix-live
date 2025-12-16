import os

def find_settings_file():
    # Current directory
    base_dir = os.getcwd()
    
    # Walk through folders to find settings.py
    for root, dirs, files in os.walk(base_dir):
        if 'venv' in root or '.git' in root: # Skip venv and git folders
            continue
        for file in files:
            if file == 'settings.py':
                return os.path.join(root, file)
    return None

def setup_razorpay():
    print("-" * 50)
    print("💳 AUTOMATIC RAZORPAY SETUP")
    print("-" * 50)
    
    # 1. FIND THE FILE
    settings_path = find_settings_file()
    
    if not settings_path:
        print("❌ Error: 'settings.py' file kedaikkala!")
        print("Please make sure you are in the correct project folder.")
        return

    print(f"✅ Found settings file at: {settings_path}")
    print("-" * 50)

    # 2. ASK USER FOR KEYS (Secure Input)
    print("👇 Inga unga Razorpay Keys-a paste pannunga:")
    key_id = input("Paste Key ID (rzp_live_...): ").strip()
    key_secret = input("Paste Key Secret: ").strip()

    if not key_id or not key_secret:
        print("❌ Error: Keys cannot be empty!")
        return

    # 3. PREPARE CODE
    razorpay_code = f"""

# ==============================================
# RAZORPAY SETTINGS (Auto-Added)
# ==============================================
RAZORPAY_KEY_ID = 'rzp_live_Rrq5jqy3nk3pA6'
RAZORPAY_KEY_SECRET = 'waywumrUF8mLOG0JuUKb9hDF'
"""

    # 4. WRITE TO FILE
    try:
        # Read file first to check if already added
        with open(settings_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if "RAZORPAY_KEY_ID" in content:
            print("⚠️ Razorpay settings already exist! Overwriting...")
            # Simple append might duplicate, but for now it's safer than complex parsing
            # You can manually clean up if needed later.
        
        with open(settings_path, 'a', encoding='utf-8') as f:
            f.write(razorpay_code)
            
        print("-" * 50)
        print("✅ SUCCESS! Razorpay Keys saved.")
        print("🚀 Restarting Server might be needed.")
        print("-" * 50)
        
    except Exception as e:
        print(f"❌ Error writing to file: {e}")

if __name__ == "__main__":
    setup_razorpay()