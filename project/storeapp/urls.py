from django.contrib import admin
from django.urls import path
from.import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('',views.index,name='index'),
    path('profile_view',views.customer_Profile,name='customer_profile'),
    # path('profile_update/',views.profile,name='profile'),
    path('seller/',views.seller_index,name='seller_index'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('update_wishlist_quantity/<int:product_id>/<int:new_quantity>/', views.update_wishlist_quantity, name='update_wishlist_quantity'),
    path('seller_reg/',views.seller_reg_step,name='seller_reg_step'),
    # path('reg_step/',views.reg_step,name='reg_step'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('decrease_item/<int:item_id>/', views.decrease_item, name='decrease_item'),
    path('increase_item/<int:item_id>/', views.increase_item, name='increase_item'),
    # path('update_cart/', views.update_cart, name='update_cart'),
    path('add_product/', views.add_product, name='add_product'),
    path('shop/', views.shop, name='shop'),
    # path('sellerindex/', views.sellerindex, name='sellerindex'),

    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('contact/',views.contact,name='contact'),
    path('seller_product_listing/', views.seller_product_listing, name='seller_product_listing'),
    path('search/<str:name>', views.search_product, name='search_product'),
    path('checkout/',views.checkout,name='checkout'),
    path('update_product/<int:product_id>/', views.update_product, name='update_product'),
    path('seller_orders/', views.seller_orders, name='seller_orders'),

    path('homepage/', views.homepage, name='homepage'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('print_as_pdf/<int:cart_id>/', views.print_as_pdf, name='print_as_pdf'),
    path('my_orders/',views.my_orders,name='my_orders'),
    path('add_address/',views.add_address,name='add_address'),
    path('monthly_sales/',views.monthly_sales,name='monthly_sales'),
    
    path('low-stock-notification/<int:seller_id>/', views.low_stock_notification, name='low_stock_notification'),
    path('show_notification/<int:seller_id>',views.showNotification,name="show_notification"),
    path('mark_notifications_as_read/',views.mark_notifications_as_read,name="mark_notifications_as_read"),
    path('quality/',views.quality,name="quality"),
    path('predict/', views.predict, name='predict'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('result/', views.result, name='result'),
    path('sales_report/', views.sales_report, name='sales_report'),


    # path('notifications/', views.notification_list, name='notification_list'),
    # path('notifications/mark_as_read/', views.mark_notifications_as_read, name='mark_notifications_as_read'),


    # path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),



    # ----------------------------------admin--------------------------------------
    # path('index_admin/', views.index_admin, name='index_admin'),
    
    
    
    
    
    #-----------------MAIN----------------------------
    # path('customer_ProductView/<int:product_id>/',views.customer_ProductView,name='customer_ProductView'),
    path('add_review/<int:product_id>/', views.add_review, name='add_review'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
