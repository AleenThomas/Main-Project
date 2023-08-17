from django.contrib import admin
from django.urls import path
from.import views

urlpatterns = [
    path('',views.index,name='index'),
    path('profile_view/',views.cust_profile,name='cust_profile'),
    path('profile_update/',views.profile,name='profile'),
   
]
