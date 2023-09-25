# from django import forms
# from django.core.exceptions import ValidationError
# from .models import Product
# import re

# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['product_name', 'description', 'image', 'quantity', 'price', 'brand_name']

#     def clean_product_name(self):
#         product_name = self.cleaned_data['product_name']

#         # Check if product_name contains only letters
#         if not product_name.isalpha():
#             raise forms.ValidationError("Product name should contain only letters.")

#         return product_name

#     def clean_description(self):
#         description = self.cleaned_data['description']

#         # Check if the number of words in description is more than 30
#         if len(description.split()) > 30:
#             raise forms.ValidationError("Description should contain a maximum of 30 words.")

#         return description

#     def clean_image(self):
#         image = self.cleaned_data['image']

#         # Check if the image file format is allowed
#         if not image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
#             raise forms.ValidationError("Only .jpg, .jpeg, and .png image formats are allowed.")

#         return image

#     def clean_quantity(self):
#         quantity = self.cleaned_data['quantity']

#         # Check if quantity is a non-negative integer
#         if not isinstance(quantity, int) or quantity < 0:
#             raise forms.ValidationError("Quantity should be a non-negative integer.")

#         return quantity

# def clean_price(self):
#         price = self.cleaned_data['price']

#         # Check if the price can be converted to a float
#         try:
#             price_float = float(price)
#         except ValueError:
#             raise forms.ValidationError("Price should be a valid number.")

#         # Check if the price is non-negative
#         if price_float < 0:
#             raise forms.ValidationError("Price should be a non-negative number.")

#         return price_float

# def clean_brand_name(self):
#         brand_name = self.cleaned_data['brand_name']

#         # Check if brand_name contains only letters and digits
#         if not re.match("^[a-zA-Z0-9]+$", brand_name):
#             raise forms.ValidationError("Brand name should contain only letters and digits.")

#         return brand_name
