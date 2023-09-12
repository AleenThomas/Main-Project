from django.contrib import admin
from .models import Customer_Profile,Product,SellerDetails,Wishlist,CartItem

# Register your models here.
admin.site.register(Customer_Profile)
admin.site.register(Product)
admin.site.register(SellerDetails)
admin.site.register(Wishlist)
admin.site.register(CartItem)





