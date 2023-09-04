from django.contrib import admin
from django.urls import path
from.import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('',views.index,name='index'),
    path('profile_view/<int:user>',views.cust_profile,name='cust_profile'),
    path('profile_update/',views.profile,name='profile'),
    path('seller/',views.seller_index,name='seller_index'),
    path('add_product/', views.add_product, name='add_product'),
    path('shop/', views.shop, name='shop'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('contact/',views.contact,name='contact'),
    path('seller_product_listing/', views.seller_product_listing, name='seller_product_listing'),




   
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
