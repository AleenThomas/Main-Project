from django.contrib import admin
from django.urls import path
from.import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('',views.index,name='index'),
    path('profile_view/',views.customer_Profile,name='customer_profile'),
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
    path('order-notification/<int:seller_id>/<int:order_id>/', views.order_notification, name='order_notification'),
    path('booking-notification/<int:seller_id>/<int:farm_id>/', views.booking_notification, name='booking_notification'),

    path('quality/',views.quality,name="quality"),
    path('predict/', views.predict, name='predict'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('result/', views.result, name='result'),
    path('blog/', views.blog, name='blog'),
    path('createblog/', views.createblog, name='createblog'),
    path('farm_details/',views.farm_details,name='farm_details'),
    path('farm_view/',views.farm_view,name='farm_view'),
    path('farm_view_details/<int:farm_id>',views.farm_view_details,name='farm_view_details'),
    path('farm_booking/<int:farmbooking_id>',views.farm_booking,name='farm_booking'),
    path('booking_seller/<int:farm_id>',views.seller_booking,name='seller_booking'),
    path('generate_sales_report/', views.generate_sales_report, name='generate_sales_report'),
    path('seller_sales_report/',views.seller_sales_report,name='seller_sales_report'),
    path('seller_report/',views.seller_report,name='seller_report'),
    path(' get_most_sold_products/', views. get_most_sold_products, name=' get_most_sold_products'),

    path('process_payment/<int:booking_id>/<int:amount>/', views.process_payment, name='process_payment'),
    path('booking_result_display/<int:user_id>/',views.booking_result_display,name='booking_result_display'),
    path('seller_booking_display/',views.seller_booking_display,name='seller_booking_display'),
    # path('gifthamper/', views.gifthamper, name='gifthamper'),
    
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('update-available-rooms/', views.update_available_rooms, name='update_available_rooms'),
    path('changeDispatch/<str:cart_items>/<int:order_id>', views.changeDispatch, name='changeDispatch'),
    path( 'changeStore/<str:cart_items>/<int:order_id>', views.changeStore, name='changeStore'),

    
    path('hub_home/', views.hub_home, name='hub_home'),
    path('hub_login/', views.hub_login, name='hub_login'),
    path('hub_orders/', views.hub_orders, name='hub_orders'),
    path('delivery_registration/', views.delivery_registration, name='delivery_registration'),
    path('delivery_agent_home/', views.delivery_agent_home, name='delivery_agent_home'),
    path('delivery_agent_profile/', views.delivery_agent_profile, name='delivery_agent_profile'),






    

    # path('filter-products/', views.filter_products, name='filter_products'),


    # path('notifications/', views.notification_list, name='notification_list'),
    # path('notifications/mark_as_read/', views.mark_notifications_as_read, name='mark_notifications_as_read'),


    # path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),



    # ----------------------------------admin--------------------------------------
    # path('index_admin/', views.index_admin, name='index_admin'),
    
    
    
    
    
    #-----------------MAIN----------------------------
    # path('customer_ProductView/<int:product_id>/',views.customer_ProductView,name='customer_ProductView'),
    path('add_review/<int:product_id>/', views.add_review, name='add_review'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
