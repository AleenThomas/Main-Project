from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    # product_name=forms.CharField(
    #     widget=forms.TextInput(
    #     attrs={
    #         "class":"product"
    #         "id":"pdtid"
    #     }     
    #     )
    # )
    class Meta:
        model = Product
        fields = ['product_name', 'description', 'image', 'quantity', 'price','brand_name']
