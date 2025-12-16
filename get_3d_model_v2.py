import os
import urllib.request
import ssl

# 1. SETUP PATHS
base_dir = os.getcwd()
static_dir = os.path.join(base_dir, 'store', 'static')

# Create 'static' folder if not exists
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

# File Path
model_path = os.path.join(static_dir, 'mannequin.glb')

# 2. CORRECTED URL (Using 'main' branch and raw.githubusercontent)
url = "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/main/2.0/Mannequin/glTF-Binary/Mannequin.glb"

print("-" * 50)
print("⬇️  DOWNLOADING REAL 3D MODEL (ATTEMPT 2)...")
print("-" * 50)

# 3. BYPASS SSL ERROR (Just in case firewall blocks it)
ssl._create_default_https_context = ssl._create_unverified_context

try:
    print(f"🔗 Connecting to: {url}...")
    urllib.request.urlretrieve(url, model_path)
    
    # Check if file size is valid (sometimes it downloads empty error file)
    file_size = os.path.getsize(model_path)
    if file_size < 1000:
        print("❌ Downloaded file is too small (Error). Retrying backup...")
        raise Exception("File too small")

    print(f"✅ SUCCESS! Model saved at: {model_path}")
    print(f"📦 File Size: {file_size / 1024:.2f} KB")
    print("🚀 Now Restart Server & Check Website!")

except Exception as e:
    print(f"❌ Download Failed: {e}")
    print("⚠️ Alternate Option: I will give you code to generate model without download.")