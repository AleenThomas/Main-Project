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
    

# from django.db import models
# from django.utils import timezone
# from django.contrib.auth.models import User

class Product(models.Model):
    # Your existing fields
    product_name = models.CharField(max_length=255,null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    
    # Separate fields for quantity and its prefix
    quantity_value = models.PositiveIntegerField(default=100,null=True)
    quantity_prefix = models.CharField(max_length=10, choices=[('gms', 'gms'), ('kg', 'kg')], default='gms')
    
    stock = models.PositiveIntegerField(default=1,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    date_added = models.DateField(default=timezone.now)
    brand_name = models.CharField(max_length=255, default="",null=True)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    batch_no=models.CharField(max_length=10,default="",null=True)

    # Define choices for the status field
    STATUS_CHOICES = [
        ('In Stock', 'In Stock'),
        ('Out of Stock', 'Out of Stock'),
    ]
    
    # Add the status field
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='In Stock')

    def save(self, *args, **kwargs):
        # Update the status based on the stock value
        if self.stock == 0:
            self.status = 'Out of Stock'
        else:
            self.status = 'In Stock'
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name

    

    
# class CartItem(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)

#     def __str__(self):
#         return f"{self.quantity} x {self.product.product_name}"


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
        
        
class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Category"

class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Subcategory"

        
class Order(models.Model):
    class PaymentStatusChoices(models.TextChoices):
            PENDING = 'pending', 'Pending'
            SUCCESSFUL = 'successful', 'Successful'
            FAILED = 'failed', 'Failed'

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True,null=True)
    razorpay_order_id = models.CharField(max_length=255, default=None)
    payment_status = models.CharField(
    max_length=20, choices=PaymentStatusChoices.choices, default=PaymentStatusChoices.PENDING)
    # date_added = models.DateField(default=timezone.now)

    # cart = models.ForeignKey(CartItem, on_delete=models.SET_NULL, null=True, blank=True)

    def _str_(self):
        return self.user.email
        
class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.quantity} x {self.product.product_name} ({'Active' if self.is_active else 'Inactive'})"
class Notification(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
class PredictionImage(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    prediction=models.CharField(max_length=120,null=True)


