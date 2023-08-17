from django.db import models

# Create your models here.
# from.models import CustomUser
# from django.contrib.auth import get_user_model

# User = get_user_model()
from userapp.models import CustomUser
from django.contrib.auth.models import AbstractUser

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default="user_avatar.jpg", blank=True, null=True)
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return self.user.name
# # class Customer(models.Model):
# # 	user = models.OneToOneField(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
# # 	name = models.CharField(max_length=200, null=True)
# # 	phone = models.CharField(max_length=200, null=True)
# # 	email = models.CharField(max_length=200, null=True)
# # 	profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
# # 	date_created = models.DateTimeField(auto_now_add=True, null=True)

# # 	def __str__(self):
# # 		return self.name