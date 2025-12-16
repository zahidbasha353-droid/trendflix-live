import os

# 1. SETUP PATHS
base_dir = os.getcwd()
store_dir = os.path.join(base_dir, 'store')
forms_path = os.path.join(store_dir, 'forms.py')

# 2. CONTENT FOR forms.py
forms_code = """from django import forms
from .models import Product

class ProductUploadForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'selling_price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Design Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tell us about your art...', 'rows': 3}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Your Selling Price (Min ₹399)'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
"""

# 3. CREATE THE FILE
if os.path.exists(store_dir):
    with open(forms_path, 'w', encoding='utf-8') as f:
        f.write(forms_code)
    print("-" * 50)
    print(f"✅ SUCCESS! Created file: {forms_path}")
    print("-" * 50)
    print("🚀 Now Restart Server: python manage.py runserver")
else:
    print("❌ ERROR: 'store' folder not found. Are you in the right directory?")