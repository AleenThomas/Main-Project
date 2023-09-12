from django.db import models
from django.utils import timezone



# Create your models here.
# from.models import CustomUser
# from django.contrib.auth import get_user_model

# User = get_user_model()
from userapp.models import CustomUser
from django.contrib.auth.models import AbstractUser

class Customer_Profile(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)

    def _str_(self):
        return self.user.email
    


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateField(default=timezone.now)
    brand_name = models.CharField(max_length=255,default="")
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True) 

    def __str__(self):
        return self.product_name
    
class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name}"


class Wishlist(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.user.username + "'s Wishlist"



# # class Customer(models.Model):
# # 	user = models.OneToOneField(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
# # 	name = models.CharField(max_length=200, null=True)
# # 	phone = models.CharField(max_length=200, null=True)
# # 	email = models.CharField(max_length=200, null=True)
# # 	profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
# # 	date_created = models.DateTimeField(auto_now_add=True, null=True)

# # 	def __str__(self):
# # 		return self.name


class SellerDetails(models.Model):
    # Step 2 Fields
    store_name = models.CharField(max_length=255,null=True)
    phone_number = models.CharField(max_length=15,null=True)
    pincode = models.CharField(max_length=10,null=True)
    pickup_address = models.CharField(max_length=255,null=True)
    city = models.CharField(max_length=100,null=True)
    state = models.CharField(max_length=100,null=True)
    
    # Step 3 Fields
    account_holder_name = models.CharField(max_length=255,null=True)
    account_number = models.CharField(max_length=20,null=True)
    bank_name = models.CharField(max_length=255,null=True)
    branch = models.CharField(max_length=255)
    ifsc_code = models.CharField(max_length=20)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='seller_details_user',null=True)

    def __str__(self):
        return self.store_name
    class Meta:
        verbose_name_plural = "SellerDetails"