import os
import urllib.request

# 1. SETUP PATHS
base_dir = os.getcwd()
static_dir = os.path.join(base_dir, 'store', 'static')

# Create 'static' folder if it doesn't exist
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
    print(f"📁 Created folder: {static_dir}")

# File Path
model_path = os.path.join(static_dir, 'mannequin.glb')

# 2. DOWNLOAD URL (Official Sample Model)
url = "https://github.com/KhronosGroup/glTF-Sample-Models/raw/master/2.0/Mannequin/glTF-Binary/Mannequin.glb"

print("-" * 50)
print("⬇️  DOWNLOADING 3D MANNEQUIN MODEL...")
print("    (This might take a few seconds depending on internet)")
print("-" * 50)

try:
    urllib.request.urlretrieve(url, model_path)
    print("✅ DOWNLOAD SUCCESS!")
    print(f"📍 File saved at: {model_path}")
    print("🚀 Now you can run the server and see the Real Person!")
except Exception as e:
    print(f"❌ Download Failed: {e}")
    print("Check your internet connection.")