from django import forms
from .models import Product

class ProductUploadForm(forms.ModelForm):
    class Meta:
        model = Product
        # பழைய 'selling_price' ஐ எடுத்துட்டு 'price' போட்டாச்சு
        fields = ['name', 'description', 'price', 'image', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }