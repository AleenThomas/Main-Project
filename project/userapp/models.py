from django.db import models
from django.contrib.auth.models import AbstractUser
# from storeapp.models import Notification
class CustomUser(AbstractUser):
    username = None
    USERNAME_FIELD  = 'email'
    # username=models.CharField(max_length=100,default='',unique=True)
    name = models.CharField(max_length=100, default='')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_customer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    gstn = models.CharField(max_length=15, blank=True, null=True) 
    hub_status=models.BooleanField(default=False)
    
    
    
    

    REQUIRED_FIELDS = []
    
    
    def unread_notification_count(self):
        return Notification.objects.filter(user=self, read=False).count()
    def __str__(self):
        return self.name
