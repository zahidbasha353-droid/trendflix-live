import os

# 1. SETUP PATH
base_dir = os.getcwd()
# CHANGE: Folder name changed from 'Trendflix_Amazon' to 'trendflix_core'
settings_path = os.path.join(base_dir, 'trendflix_core', 'settings.py') 

# ⚠️ UNGA KEYS INGA PODUNGA (Replace these)
YOUR_KEY_ID = "rzp_test_XXXXXXXXXXXXXXXX"  # <-- Inga Key ID podunga
YOUR_KEY_SECRET = "YYYYYYYYYYYYYYYYYYYYYYYY"  # <-- Inga Key Secret podunga

print("-" * 50)
print("⚙️ ADDING RAZORPAY SETTINGS AUTOMATICALLY...")
print("-" * 50)

# The Code to Append
razorpay_code = f"""

# ==============================================
# RAZORPAY PAYMENT SETTINGS (Added by Script)
# ==============================================
RAZORPAY_KEY_ID = '{YOUR_KEY_ID}'
RAZORPAY_KEY_SECRET = '{YOUR_KEY_SECRET}'
"""

# 2. APPEND TO SETTINGS.PY
try:
    with open(settings_path, 'a', encoding='utf-8') as f:
        f.write(razorpay_code)
    
    print(f"✅ SUCCESS! Razorpay settings added to: {settings_path}")
    print(f"🔑 Key ID Used: {YOUR_KEY_ID}")
    print("-" * 50)
    print("🚀 Now Restart Server: python manage.py runserver")

except FileNotFoundError:
    print("❌ ERROR: settings.py innum kedaikkala.")
    print(f"Tried path: {settings_path}")
    print("Check if 'trendflix_core' folder exists!")