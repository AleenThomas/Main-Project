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
    average_rating = models.FloatField(default=0.0)

    # Define choices for the status field
    STATUS_CHOICES = [
        ('In Stock', 'In Stock'),
        ('Out of Stock', 'Out of Stock'),
    ]
    
    # Add the status field
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='In Stock')
    category = models.CharField(max_length=100, null=True)
    subcategory = models.CharField(max_length=100, null=True)

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

class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    house_building = models.CharField(max_length=100)
    road_area_colony = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    phone = models.CharField(max_length=10)

    
    
    
class Order(models.Model):
    class PaymentStatusChoices(models.TextChoices):
            PENDING = 'pending', 'Pending'
            SUCCESSFUL = 'successful', 'Successful'
            FAILED = 'failed', 'Failed'
    class OrderStatusChoices(models.TextChoices):
        REQUESTED = 'Requested', 'Requested'
        DISPATCHED = 'Dispatched', 'Dispatched'
        DELIVERED = 'Delivered', 'Delivered'


    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(default=timezone.now,null=True)
    razorpay_order_id = models.CharField(max_length=255, default=None)
    payment_status = models.CharField(
    max_length=20, choices=PaymentStatusChoices.choices, default=PaymentStatusChoices.PENDING)
    order_status = models.CharField(
        max_length=20, choices=OrderStatusChoices.choices, default=OrderStatusChoices.REQUESTED)
    accepted_by_store = models.BooleanField(default=False)
    ready_for_pickup = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)

    address = models.ForeignKey(Address, on_delete=models.CASCADE) # Adding the foreign key to Address model

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
    dispatched = models.BooleanField(default=False)  
    accepted_by_store = models.BooleanField(default=False)
    ready_for_pickup = models.BooleanField(default=False) 


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
    
    
from django.db.models import Avg
class CustomerReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sentiment_score = models.FloatField(null = True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update the average rating of the associated product
        self.product.average_rating = CustomerReview.objects.filter(product=self.product).aggregate(Avg('rating'))['rating__avg'] or 0
        self.product.save()


class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)

    def __str__(self):
        return self.title
    
class Farm(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    farm_name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    description = models.TextField()
    activities = models.TextField()
    visiting_hours_from = models.CharField(max_length=100,null=True)
    visiting_hours_to = models.CharField(max_length=100,null=True)

    contact_info = models.CharField(max_length=100)
    image = models.ImageField(upload_to='farm_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.farm_name
class Farm_Booking(models.Model):
    farm_id=models.ForeignKey(Farm,on_delete=models.CASCADE,default=1)
    stay_name=models.CharField(max_length=100)
    rooms=models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True) 
    
    def __str__(self):
        return self.stay_name 
class SaveBooking(models.Model):
    class BookingStatusChoices(models.TextChoices):
            PENDING = 'pending', 'Pending'
            SUCCESSFUL = 'successful', 'Successful'
            FAILED = 'failed', 'Failed'
    farm=models.ForeignKey(Farm_Booking, on_delete=models.CASCADE,default=2)
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE,default=6)
    total_price=models.DecimalField(max_digits=10, decimal_places=2,null=True)
    name=models.CharField(max_length=100)
    phone_no=models.CharField(max_length=15,null=True)
    rooms_booked=models.PositiveIntegerField(default=1,null=True)
    # available_rooms = models.PositiveIntegerField(default=1)  # New field for available rooms
    rooms_updated = models.BooleanField(default=False)
    check_in= models.DateField(default=timezone.now)
    check_out= models.DateField(default=timezone.now)
    adults=models.PositiveIntegerField(default=0,null=True)
    children=models.PositiveIntegerField(default=0,null=True)
    status = models.CharField(
    max_length=20, choices=BookingStatusChoices.choices, default=BookingStatusChoices.PENDING) 
    
    def __str__(self):
        return self.name 
    
class DeliveryAgent(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,default=22)

    phone_number = models.CharField(max_length=15)
    vehicle_type = models.CharField(max_length=20)
    license_number = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    id_proof = models.ImageField(upload_to='id_proof/')
    locality = models.CharField(max_length=255)
    registration_date = models.DateTimeField(auto_now_add=True)
    
