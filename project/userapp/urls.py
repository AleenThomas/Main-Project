from django.contrib import admin
from django.urls import path,include
from.import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.customer_register,name='customer_register'),
    path('sellerregister',views.seller_register,name='seller_register'),
    path('login/',views.custom_login,name='custom_login'),
    path('logout/',views.logout,name='logout'),
    
    path("accounts/", include("allauth.urls")),

    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    
]
 