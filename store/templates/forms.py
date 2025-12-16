from django import forms
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