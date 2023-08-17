from django.db import models
from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):
    username = None
    USERNAME_FIELD  = 'email'
    name = models.CharField(max_length=100, default='')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_customer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.name
