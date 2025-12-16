from django import forms
from .models import Product

class ProductUploadForm(forms.ModelForm):
    class Meta:
        model = Product
        # இங்கே selling_price க்கு பதில் price போட்டாச்சு
        fields = ['name', 'description', 'price', 'image', 'category'] 
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe your design...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Set your price (e.g., 499)'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }