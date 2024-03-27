from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from .models import Customer_Profile
# from .forms import ProductForm
from .models import *
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from decimal import Decimal
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from xhtml2pdf import pisa
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from django.utils import timezone

# from .models import booknow, On_payment

def index(request):
    
    user=request.user
    product_ids, product_names = get_most_sold_products()
    list1=[]
    for i in product_ids:
        var=Product.objects.get(id=i)
        list1.append(var)
    print(list1)
    products_with_sentiment_sum = Product.objects.annotate(sentiment_sum=Sum('customerreview__sentiment_score')).order_by('-sentiment_sum')[:3]
    for product in products_with_sentiment_sum:
        print (product.product_name)
    if user.is_anonymous:
        return render(request, 'index.html', {'products_with_sentiment_sum' :products_with_sentiment_sum ,'product_ids': list1,})

    elif user.is_seller==True:
        return redirect('seller_index')
    else:
        update_available_rooms(request)

        
        return render(request, 'index.html', {'products_with_sentiment_sum' : products_with_sentiment_sum,'product_ids': list1,
                                               })
    # return render(request,'index.html')
    
def contact(request):
    return render(request,'contact.html')
@never_cache
def loginredirect(request):
    return render(request,'login_redirect.html')
# def sellerindex(request):
#     return render(request,'sellerindex.html')
# def reg_step(request):
#     return render(request,'reg_step.html')

@login_required(login_url='loginredirect')
@never_cache
def wishlist_view(request):
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.get_or_create(user=request.user)[0]
        wishlist_products = wishlist.products.all()
        return render(request, 'wishlist.html', {'wishlist_products': wishlist_products})
    else:
        return render(request, 'login_required.html')

@login_required(login_url='loginredirect')
def add_to_wishlist(request, product_id):
    products_with_sentiment_sum = Product.objects.annotate(sentiment_sum=Sum('customerreview__sentiment_score')).order_by('-sentiment_sum')[:3]
    for product in products_with_sentiment_sum:
        print (product.product_name)
    product = get_object_or_404(Product, pk=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    message = 'Product added to wishlist'
    return render(request, 'index.html', {'message': message,'products_with_sentiment_sum' : products_with_sentiment_sum})
@login_required(login_url='loginredirect')
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    wishlist = get_object_or_404(Wishlist, user=request.user)
    wishlist.products.remove(product)
    success_message = f'{product.product_name} removed from your wishlist.'

    # You can pass the success_message to the template
    return redirect('wishlist')
def update_wishlist_quantity(request, product_id, new_quantity):
    try:
        new_quantity = int(new_quantity)
    except ValueError:
        return JsonResponse({'message': 'Invalid quantity'}, status=400)
    
    if new_quantity <= 0:
        return JsonResponse({'message': 'Quantity must be greater than zero'}, status=400)
    
    product = get_object_or_404(Product, pk=product_id)
    wishlist = get_object_or_404(Wishlist, user=request.user)
    
    # Update the quantity of the product in the wishlist
    item = wishlist.wishlist_items.filter(product=product).first()
    if item:
        item.quantity = new_quantity
        item.save()
        return JsonResponse({'message': 'Quantity updated successfully'})
    else:
        return JsonResponse({'message': 'Product not found in wishlist'}, status=404)




@never_cache
def seller_reg_step(request):
    if request.method == 'POST':
        step = request.POST.get('step')

        print(step)
        # Check which step the form data is coming from
        if step == '1':
            email = request.user.email  # Get the email from the logged-in user
            gstn = request.POST.get('gstn')  # GSTN from the form

            # Check for existing user with the same email
            if CustomUser.objects.filter(email=email).exists():
                user = CustomUser.objects.get(email=email)
                user.is_seller = True  # Set the user as a seller
                user.save()

                # Check if the user already has seller details
                seller_details, created = SellerDetails.objects.get_or_create(user=user)

                # Update the seller details
                seller_details.gstn = gstn
                seller_details.save()

                messages.success(request, "Step 1 completed successfully.")

                # Store the user ID in the session for future steps
                request.session['user_id'] = user.id

                messages.success(request, "Step 1 completed successfully.")
                # Redirect to step 2 or confirmation page

        elif step == '2':
            print("two")
            # Step 2 Data
            user_id = request.session.get('user_id')
            if user_id:
                user = CustomUser.objects.get(id=user_id)
                
                store_name = request.POST.get('store-name')
                phone_number = request.POST.get('phone-number')
                pincode = request.POST.get('pincode')
                pickup_address = request.POST.get('pickup-address')
                city = request.POST.get('city')
                state = request.POST.get('state')

                # Check if the user already has seller details
                seller_details, created = SellerDetails.objects.get_or_create(user=user)

                # Update the seller details
                seller_details.store_name = store_name
                seller_details.phone_number = phone_number
                seller_details.pincode = pincode
                seller_details.pickup_address = pickup_address
                seller_details.city = city
                seller_details.state = state
                seller_details.save()

                messages.success(request, "Step 2 completed successfully.")
                # Redirect to step 3 or confirmation page

        elif step == '3':
            print("three")
            # Step 3 Data
            user_id = request.session.get('user_id')
            if user_id:
                user = CustomUser.objects.get(id=user_id)
                
                account_holder_name = request.POST.get('account-holder-name')
                account_number = request.POST.get('account-number')
                bank_name = request.POST.get('bank-name')
                branch = request.POST.get('branch')
                ifsc_code = request.POST.get('ifsc-code')

                # Check if the user already has seller details
                seller_details, created = SellerDetails.objects.get_or_create(user=user)

                # Update the seller details
                seller_details.account_holder_name = account_holder_name
                seller_details.account_number = account_number
                seller_details.bank_name = bank_name
                seller_details.branch = branch
                seller_details.ifsc_code = ifsc_code
                seller_details.save()

                messages.success(request, "Step 3 completed successfully.")
                # Redirect to confirmation page or other steps

    return render(request, 'seller_reg_step.html')



@never_cache
def seller_index(request):
    if request.user.is_seller:
        current_seller = request.user
        seller_products = Product.objects.filter(seller=current_seller)
        notification=Notification.objects.filter(seller_id=current_seller.id,read=False).count()

        # Calculate total amount, unique customers, and total orders for each product
        # product_data = []
        # total_orders_all = 0
        # unique_customers_all = 0
        # total_amount_all = 0

        # for product in seller_products:
        #     total_orders = Order.objects.filter(products=product).count()
        #     unique_customers = Order.objects.filter(products=product).values('user').distinct().count()
        #     total_amount = total_orders * product.price  
            
            # total_orders_all += total_orders
            # unique_customers_all += unique_customers
            # total_amount_all += total_amount

            # product_data.append({
            #     'product': product,
            #     'total_orders': total_orders,
            #     'unique_customers': unique_customers,
            #     'total_amount': total_amount
            # })
            # total_orders_all += total_orders
            # unique_customers_all += unique_customers
            # total_amount_all += total_amount

            # product_data.append({
            #     'product': product,
            #     'total_orders': total_orders,
            #     'unique_customers': unique_customers,
            #     'total_amount': total_amount
            # })


         # Get seller's sales report
        total_orders = Order.objects.filter(products__seller=current_seller).count()
        total_sales = Order.objects.filter(products__seller=current_seller, payment_status=Order.PaymentStatusChoices.SUCCESSFUL).aggregate(total_sales=Sum('total_price'))['total_sales'] or 0
        unique_customers = Order.objects.filter(products__seller=current_seller).values('user').distinct().count()

        context = {
            'seller_products': seller_products,
            'notification': notification,
            'total_orders': total_orders,
            'total_sales': total_sales,
            'unique_customers': unique_customers
        }
        print(total_sales)
        # context = {
        #     'seller_products': seller_products,
        #     'product_data': product_data,
        #     'total_orders_all': total_orders_all,
        #     'unique_customers_all': unique_customers_all,
        #     'total_amount_all': total_amount_all,
        #     'total_amount':total_amount,
        #     'unique_customers': unique_customers,
        #     'total_orders': total_orders,
        #     'notification':notification



        # }

        return render(request, 'sellerindex.html', context)
    else:
        return redirect('seller_reg_step')


from django.db.models import Avg

@never_cache    
def shop(request):
    # Get products added by the suppliers
    supplier_products = Product.objects.all()  # You can add filters if needed
    paginator = Paginator(supplier_products, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    average_rating = supplier_products.aggregate(Avg('average_rating')).get('average_rating', 0)
    
    context = {
        'supplier_products': supplier_products,
        'page':page,
        'average_rating': average_rating,
        
        
        
    }
    return render(request, 'shop.html', context)

# @login_required
@never_cache

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = CustomerReview.objects.filter(product=product)
    print(reviews)
    # Fetch related products and reviews
    related_products = Product.objects.filter(
        status__in=['in_stock', 'out_of_stock']
    ).exclude(pk=product_id)[:4]

    reviews = CustomerReview.objects.filter(product=product)
    if request.user.is_authenticated:
            user_has_purchased_product = Order.objects.filter(
            user=request.user,
            cartitem__product=product,
            payment_status=Order.PaymentStatusChoices.SUCCESSFUL
        ).exists()
   
    print(user_has_purchased_product)
    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'user_has_purchased_product': user_has_purchased_product
    }

    return render(request, 'shop-single.html',context)

@login_required(login_url='user_login')
def customer_ProductView(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product_category = product.product_category
    product_subcategory = product.product_subcategory

    # Fetch related products and reviews
    related_products = Product.objects.filter(
        product_category=product_category,
        status__in=['in_stock', 'out_of_stock']
    ).exclude(pk=product_id)[:4]

    reviews = CustomerReview.objects.filter(product=product)
    if request.user.is_authenticated:
            user_has_purchased_product = Order.objects.filter(
            user=request.user,
            cart_items__product=product,
            payment_status=Order.PaymentStatusChoices.SUCCESSFUL
        ).exists()
   
    print(user_has_purchased_product)
    context = {
        'product': product,
        'product_category': product_category,
        'product_subcategory': product_subcategory,
        'related_products': related_products,
        'reviews': reviews,
        'user_has_purchased_product': user_has_purchased_product
    }

    return render(request, 'shop-single.html', context)

import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
@login_required
def add_review(request, product_id):
    # product = get_object_or_404(Product, pk=product_id)
    # if request.method == 'POST':
    #     rating = int(request.POST.get('rating'))
    #     comment = request.POST.get('comment')

    #     # Check if the user has ordered the product
    #     has_ordered_product = Order.objects.filter(user=request.user, products=product, payment_status=Order.PaymentStatusChoices.SUCCESSFUL).exists()

    #     if has_ordered_product:
    #         # Check if the user has already reviewed the product
    #         existing_review = CustomerReview.objects.filter(product=product, user=request.user).exists()

    #         if not existing_review:
    #             # Create a new review
    #             review = CustomerReview.objects.create(product=product, user=request.user, rating=rating, comment=comment)
    #             messages.success(request, 'Thank you for your review! Your feedback is valuable.')
    #             return redirect('product_detail', product_id=product_id)
    #         else:
    #             messages.error(request, 'You have already reviewed this product.')
    #     else:
    #         messages.error(request, 'You must order this product before reviewing. Make a purchase to share your thoughts with us!')


    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment')
        sentiment_analyzer = SentimentIntensityAnalyzer()
        sentiment_score = sentiment_analyzer.polarity_scores(comment)['compound']
        
        # Check if the user has already reviewed the product
        existing_review = CustomerReview.objects.filter(product=product, user=request.user).exists()
        

        if not existing_review:
            # Create a new review
            review = CustomerReview.objects.create(product=product, user=request.user, rating=rating, comment=comment, sentiment_score=sentiment_score)
            return redirect('product_detail', product_id=product_id)
        else:
            return JsonResponse({'success': False, 'message': 'You have already reviewed this product.'})

    return redirect('product_detail', product_id=product_id)

@never_cache
@login_required(login_url='loginredirect')
def seller_product_listing(request):
    if request.user.is_seller:
        current_seller = request.user
        seller_products = Product.objects.filter(seller=current_seller)
    
        context = {
            'seller_products': seller_products
        }
    
        return render(request, 'product_list.html', context)
    else:
        # If the logged-in user is not a seller, you can redirect them or show an error message
        # For example, you can redirect them to a page where they can register as a seller
        return redirect('seller_register')



@login_required(login_url='loginredirect')
def add_product(request):
    if request.user.is_seller:
        if request.method == 'POST':
            # Retrieve form data from the request
            product_name = request.POST.get('product_name')
            description = request.POST.get('description')
            image = request.FILES.get('image')
            quantity_value = request.POST.get('quantity')  # Updated field name
            quantity_prefix = request.POST.get('quantity-prefix')  # Updated field name
            price = request.POST.get('price')
            brand_name = request.POST.get('brand_name')
            stock = request.POST.get('stock')
            category = request.POST.get('category')  # Retrieve category from the form
            subcategory = request.POST.get('subcategory') 

            # Validate the form data here if needed
            # You can use your ProductForm for validation

            # Create and save the product
            product = Product(
                product_name=product_name,
                description=description,
                image=image,
                quantity_value=quantity_value,  # Updated field name
                quantity_prefix=quantity_prefix,  # Updated field name
                price=price,
                brand_name=brand_name,
                stock=stock,
                category=category,  # Save the category to the product
                subcategory=subcategory,
                seller=request.user  # Assign the logged-in seller to the product
            )
            product.save()
            return redirect('seller_index')  # Redirect to a page showing the list of products
        else:
            # Render the empty form on a GET request
            return render(request, 'add_product.html')
    else:
        # If the logged-in user is not a seller, you can redirect them or show an error message
        # For example, you can redirect them to a page where they can register as a seller
        return redirect('seller_register')





# @login_required(login_url='custom_login')  # Redirects to the login page if not logged in
# def add_product(request):
#     if request.user.is_seller:
#         if request.method == 'POST':
#             form = ProductForm(request.POST, request.FILES)
#             if form.is_valid():
#                 product = form.save(commit=False)
#                 product.seller = request.user  # Assign the logged-in seller to the product
#                 product.save()
#                 return redirect('index')  # Redirect to a page showing the list of products
#         else:
#             form = ProductForm()

#         return render(request, 'add_product.html', {'form': form})
#     else:
#         # If the logged-in user is not a seller, you can redirect them or show an error message
#         # For example, you can redirect them to a page where they can register as a seller
#         return redirect('seller_register') 




# def update(request,update_id):
#     task=Product.objects.get(id=update_id) 
#     form=create_form(request.POST or None,instance=task) 
#     if form.is_valid():
#         form.save()
#         return redirect('table')
#     return render(request,'update.html',{'form':form})






@login_required(login_url='loginredirect')
def customer_Profile(request):
    user_profile, created = Customer_Profile.objects.get_or_create(customer=request.user)
    # farm_booking = Farm_Booking.objects.filter(user=request.user).order_by('-created_at').first()


    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile_number = request.POST.get('mobile_number')

        # Update the user profile fields
        user_profile.first_name = first_name
        user_profile.last_name = last_name
        user_profile.mobile_number = mobile_number
        user_profile.save()

        messages.success(request, 'Profile added successfully')  # Display a success message
        return redirect('customer_profile') 
    context = {
        

        'user_profile': user_profile,
        'form_submitted': request.method == 'POST',
    }
    return render(request,'custprofile.html', context)


@login_required(login_url='loginredirect')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # cart_item = CartItem.objects.get_or_create(user=request.user, product_id=product.id)
    if product.stock <= 0:
        messages.warning(request, f"{product.product_name} is out of stock.")
    else:
        cart_item,created = CartItem.objects.get_or_create(user=request.user, product_id=product.id)
        if not created:
            cart_item.is_active = True  # Set is_active to True when adding a new item to the cart

            cart_item.quantity += 1
            cart_item.save()
        else:
            
            cart_item.is_active = True  # Set is_active to True when adding a new item to the cart
            cart_item.save()

    return redirect('shop')

@login_required(login_url='loginredirect')
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    total_items = sum(item.quantity for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_items': total_items,
        'total_price': total_price,
        # ... other context variables ...
    }
    return render(request, 'cart.html',context)

def remove_from_cart(request, product_id):
    cart_item = get_object_or_404(CartItem, user=request.user, id=product_id)
    print(f"Received product_id: {product_id}")  #Fixed the typo here
    cart_item.is_active = False
    cart_item.delete()
    return redirect('cart')




def decrease_item(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            cart_item.product.stock+=1
       
    except CartItem.DoesNotExist:
        pass  # Handle the case when the item does not exist in the cart
    return redirect('cart')  # Redirect back to the cart page after decreasing the item quantity

def increase_item(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id)

        if cart_item.product.stock > 0:
            cart_item.quantity += 1
            cart_item.save()
            cart_item.product.save()
            cart_item.product.stock -= 1

        else:
            messages.warning(request, f"{cart_item.product.product_name} is out of stock.")
    except CartItem.DoesNotExist:
        pass  # Handle the case when the item does not exist in the cart
    return redirect('cart')






# -------------------------------------------------admin---------------------------------------------------
# def index_admin(request):
#     return render(request,'admin\indexadmin.html')


from django.http import JsonResponse
from .models import Product  # Make sure to import your Product model

def search_product(request, name):
    print(name)
    
    # Perform the search using a Q object to filter the Product model
    results = Product.objects.filter(product_name__icontains=name)
    
    # Serialize the results to JSON
    serialized_results = []
    
    if results.exists():  # Check if there are any results
        for result in results:
            serialized_results.append({
                'id': result.id,
                'name': result.product_name,
                'image': result.image.url
            })
            print(result.id)
    else:
        print("No results found.")

    return JsonResponse({'results': serialized_results})

    
def checkout(request):
    return render(request,'checkout.html')

@never_cache
def update_product(request, product_id):
    # Get the product object from the database using the product_id
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # Handle the form submission for updating the product
        product_name = request.POST.get('product_name', product.product_name)
        description = request.POST.get('description', product.description)
        image = request.FILES.get('image', product.image)
        quantity = request.POST.get('quantity', product.quantity_value)
        price = request.POST.get('price', product.price)
        brand_name = request.POST.get('brand_name', product.brand_name)
        stock = request.POST.get('stock', product.stock)

        # Update the product data only if new values are provided
        if product_name != product.product_name:
            product.product_name = product_name
        if description != product.description:
            product.description = description
        if image:
            product.image = image
        if quantity != product.quantity_value:
            product.quantity_value = quantity
        if price != product.price:
            product.price = price
        if brand_name != product.brand_name:
            product.brand_name = brand_name
        if stock != product.stock:
            product.stock = stock

        # Save the updated product data to the database
        product.save()
        
        # Redirect to the product detail page for the updated product
        return redirect('seller_product_listing')  # Change 'product_detail' to your desired URL name
    else:
        # If it's a GET request, render the form with the current product data
        return render(request, 'editproduct.html', {'product': product})

# def update_product(request, product_id):
#     # Get the product object from the database using the product_id
#     product = get_object_or_404(Product, id=product_id)

#     if request.method == 'POST':
#         # Retrieve form data from the request
#         product_name = request.POST.get('product_name')
#         description = request.POST.get('description')
#         image = request.FILES.get('image')
#         quantity = request.POST.get('quantity')
#         price = request.POST.get('price')
#         brand_name = request.POST.get('brand_name')
#         stock = request.POST.get('stock')

#         # Update the product data
#         product.product_name = product_name
#         product.description = description
#         product.image = image
#         product.quantity = quantity
#         product.price = price
#         product.brand_name = brand_name
#         product.stock = stock

#         # Save the updated product data to the database
#         product.save()
#         return redirect('add_product')  # Redirect to the product detail page
#     else:
#         # If it's a GET request, render the form with the current product data
#         return render(request, 'editproduct.html', {'product': product})


# def delete_product(request, product_id):
#     # Get the product instance to delete
#     product = get_object_or_404(Product, pk=product_id)

#     if request.method == 'POST':
#         # Update the product's status to 'Out of Stock' instead of deleting it
#         product.status = 'Out of Stock'
#         product.save()
#         return redirect('seller_product_listing')  # Redirect to the seller's product listing page or another appropriate page

#     # Render a confirmation page for changing the product's status
#     return render(request, 'product_list.html', {'product': product})







from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))



def homepage(request):
    cart_items = CartItem.objects.filter(user=request.user,is_active=True)
    total_price = Decimal(sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items))
    
    currency = 'INR'

    # Set the 'amount' variable to 'total_price'
    amount = int(total_price * 100)
    
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount,
        currency=currency,
        payment_capture='0'
    ))

    # Order id of the newly created order
    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler/'

    # Create the order but don't save it yet
    order = Order(
        user=request.user,
        total_price=total_price,
        razorpay_order_id=razorpay_order_id,
        payment_status=Order.PaymentStatusChoices.PENDING,
    )

    # Save the order to generate an order ID
    order.save()

    # Associate the cart items with the order
    for cart_item in cart_items:
        cart_item.order = order
        cart_item.save()
    order.save()
    # Create a context dictionary with all the variables you want to pass to the template
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,  # Set to 'total_price'
        'currency': currency,
        'callback_url': callback_url,
    }

    return render(request, 'homepage.html', context=context)

@csrf_exempt
def paymenthandler(request):
    print("payment")
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')

        # Verify the payment signature.
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        result = razorpay_client.utility.verify_payment_signature(params_dict)

        if result is False:
            # Signature verification failed.
            return render(request, 'payment/paymentfail.html')
        else:
            # Signature verification succeeded.
            # Retrieve the order from the database
            order = Order.objects.get(razorpay_order_id=razorpay_order_id)

            # Capture the payment with the amount from the order
            amount = int(order.total_price * 100)  # Convert Decimal to paise
            razorpay_client.payment.capture(payment_id, amount)

            # Update the order with payment ID and change status to "Successful"
            order.payment_id = payment_id
            order.payment_status = Order.PaymentStatusChoices.SUCCESSFUL
            
            order.save()

            # Get the associated cart items for this order
            cart_items = CartItem.objects.filter(order=order)
            
            if cart_items.exists():
                for cart_item in cart_items:
                    product = cart_item.product
                    product.stock -= cart_item.quantity
                    product.save()
                    
                    
                    
                    # Add the purchased product to the order
                    order.products.add(product)  # Associate the product with the order
                    order_notification(product.seller.id, product.id)
                # Get the cart_id from the first cart item
                cart_id = cart_items.first().id
                cart_items.update(is_active=False)
                
                # Redirect to a success page with the cart_id
                return HttpResponseRedirect(reverse('print_as_pdf', args=[cart_id]))
            else:
                # Cart items not found for the order
                return HttpResponse('No cart items found for the order.')

    
@login_required(login_url='loginredirect')
def print_as_pdf(request, cart_id):
    try:
        # Get the cart based on cart_id and make sure it belongs to the logged-in user
        cart = CartItem.objects.get(id=cart_id, user=request.user, order__isnull=False)
        # print(cart_id)
        # Ensure that the cart has a valid order associated with it
        if cart.order is None:
            raise CartItem.DoesNotExist

        cart_items = CartItem.objects.filter(order=cart.order)
        total_cost = Decimal(sum(item.product.price * item.quantity for item in cart_items))
        total=[]
        for i in cart_items:
            
            total_items=i.product.price * i.quantity
            total.append(total_items)
        # Get the user's name
        user_name = request.user.name
        date_order=datetime.now()

        # Render the HTML template to a string
        context = {
            'cart_id': cart_id,
            'cart_items': cart_items,
            'total_cost': total_cost,
            'user_name': user_name,
            'date_order':date_order,
            
        }
        # cart_items.update(quantity=0, is_active=False)
        html = render_to_string('print_invoice.html', context, request=request)

        # Create a PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{cart_id}.pdf"'

        # Generate the PDF file from the HTML content
        pisa_status = pisa.CreatePDF(html, dest=response, link_callback=None)

        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        cart_items.update(is_active=False,quantity=0)
        

        return response
    except CartItem.DoesNotExist:
        # Handle the case where the cart doesn't exist, doesn't belong to the user, or has no order
        return HttpResponse('Cart not found or does not belong to the user or has no valid order.')






# @login_required
# def my_orders(request):
#     # Assuming you have a user authentication system, get the current user
#     user = request.user
#     current_month = datetime.now().month
#     current_year = datetime.now().year

#     # Get the selected month and year from the form, or use the current month by default
#     selected_month = request.GET.get('selected_month', datetime.now().strftime('%Y-%m'))

#     # Convert the selected_month string to a datetime object
#     selected_date = datetime.strptime(selected_month, '%Y-%m')

#     # Retrieve a list of orders for the current user and the selected month
#     orders = Order.objects.filter(user=user, order_date__year=selected_date.year, order_date__month=selected_date.month).order_by('-order_date')
#     print(orders)
#     for order in orders:
#         products = order.products.all()
#         print(products)
#     print(['product_name', 'quantity', 'image_url', 'total_price'])
#     context = {
#         'orders': orders, 
#         'selected_month': f"{current_month}/{current_year}",        
#         'product_fields': ['product_name', 'quantity', 'image_url', 'total_price'],
#     }

#     # Check if there are no orders for the selected month and display a message
#     if not orders:
#         context['no_orders_message'] = 'No orders found for the selected month.'

#     return render(request, 'my_orders.html', context)



@login_required
def my_orders(request):
    # Assuming you have a user authentication system, get the current user
    user = request.user
    
    # Get the selected start_date and end_date from the form or request parameters
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    # If the start_date and end_date parameters are not provided, use the current month's date range
    if not start_date_str or not end_date_str:
        today = datetime.now()
        start_date = today.replace(day=1)  # First day of the current month
        end_date = today.replace(day=1, month=today.month + 1)  # First day of the next month

        # Format dates as strings in the 'YYYY-MM-DD' format
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')

    else:
        # Convert the start_date and end_date strings to datetime objects
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    # Retrieve a list of orders for the current user within the specified date range
    orders = Order.objects.filter(user=user, order_date__range=(start_date, end_date)).order_by('-order_date')
    sorders = Order.objects.filter(
    Q(user=user) & 
    Q(payment_status=Order.PaymentStatusChoices.SUCCESSFUL)
)
    # Rest of your code...

    context = {
        'orders': orders,
        'start_date': start_date_str,
        'end_date': end_date_str,
        'sorders':sorders,
        # ...other context data...
    }
    # print("hh"+sorders)
    # Check if there are no orders for the selected date range and display a message
    if not orders:
        context['no_orders_message'] = 'No orders found for the selected date range.'

    return render(request, 'my_orders.html', context)






    
# commented for combining
    
# @login_required
# def seller_orders(request):
#     if request.user.is_seller:
#         current_seller = request.user
#         seller_products = Product.objects.filter(seller=current_seller)
#         product_sales = []

#         for product in seller_products:
#             orders = Order.objects.filter(products=product)
#             total_amount = sum(order.total_price for order in orders)
#             product_sales.append({
#                 'product': product,
#                 'total_sold': len(orders),
#                 'total_amount': total_amount,
#                 'unique_customers': orders.values('user').distinct().count()
#             })
#         context = {
#             'product_sales': product_sales
#         }
    

#         return render(request, 'seller_orders.html', context)
#     else:
#         return redirect('seller_register')



@login_required
def monthly_sales(request):
    if request.user.is_seller:
        current_month = timezone.now().month
        current_year = timezone.now().year
        seller_products = Product.objects.filter(seller=request.user)
        product_sales = []

        for product in seller_products:
            monthly_sales = Order.objects.filter(
                products=product,
                order_date__month=current_month,
                order_date__year=current_year
            ).aggregate(
                total_sold=Count('id'),
                total_amount=Sum('total_price')
            )

            product_sales.append({
                'product': product,
                'total_sold': monthly_sales['total_sold'],
                'total_amount': monthly_sales['total_amount'] or 0
            })

        context = {
            'product_sales': product_sales
        }

        return render(request, 'salesmonth.html', context)
    else:
        return redirect('seller_register')
    








# Example: Creating a notification when a product's stock is low
from django.db.models import Q
@login_required
def low_stock_notification(request, seller_id):
    products=Product.objects.filter(seller_id=seller_id)
    for i in products:
        if i.stock<5:
            existing_notification = Notification.objects.filter(
                Q(seller_id=seller_id) & Q(message__icontains=i.product_name)
            ).exists()
            if not existing_notification:


                stock=Notification(
                    seller_id=seller_id,
                    message="The product "+i.product_name+" is on low stock with "+str(i.stock),
                )
                stock.save()
    return redirect("seller_index")
@login_required
def showNotification(request,seller_id):
    notifications=Notification.objects.filter(seller_id=seller_id)
    return render(request,"notification_list.html",{'notifications':notifications})
@login_required
def mark_notifications_as_read(request):
    noti=Notification.objects.filter(seller_id=request.user.id,read=False)
    noti.delete()
    return redirect('seller_index')



def order_notification(seller_id, product_id):
    # Retrieve the order
    print("function")
    
    # Assuming you have a list of products in the order
    

    product=Product.objects.get(id=product_id)
    print(product_id)
        # Create a notification for the seller if the product is associated with the seller
    if product.seller_id == seller_id:
        print("if")
        notification = Notification(
            seller_id=seller_id,
            message=f"An order for the product {product.product_name} has been placed."
        )
        notification.save()

    

import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
def quality(request):
    if request.method == 'POST':
        img = request.FILES.get('image')
        img2 = request.FILES.get('image')
        print(img)
        
        # Check if the uploaded file is an image (you may want to add additional validation)
        if img.content_type.startswith('image'):
            model = load_model("models/Coffee.h5")
            
            # Read image data from the InMemoryUploadedFile
            img_data = img.read()
            
            # Load the image from the image data
            img = image.load_img(io.BytesIO(img_data), target_size=(224, 224))
            img = image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            img = img / 255.0  # Normalize the image
            print(img)
            wict = model.predict(img)
            predicted_class_index = np.argmax(predict)
            print("Helllllllloooooooooo",predicted_class_index)
            class_names = ["Dark", "Green", "Light", "Medium"]  # Update with your actual class names
            predicted_class = class_names[predicted_class_index]
            pred=PredictionImage(
                user_id=request.user.id,
                image=img2,
                prediction=predicted_class
            )
            pred.save()
            return render(request, "quality_check.html",{'prediction':predicted_class,'img':pred.image})
        else:
            print("The uploaded file is not an image.")
    
    return render(request, "quality_check.html")
# def quality(request):
#     if request.method == 'POST':
#         img = request.FILES.get('image')
#         img2 = request.FILES.get('image')
#         print(img)
        
#         # Check if the uploaded file is an image (you may want to add additional validation)
#         if img.content_type.startswith('image'):
#             model = load_model("models/Cardamon_1.h5")
            
#             # Read image data from the InMemoryUploadedFile
#             img_data = img.read()
            
#             # Load the image from the image data
#             img = image.load_img(io.BytesIO(img_data), target_size=(224, 224))
#             img = image.img_to_array(img)
#             img = np.expand_dims(img, axis=0)
#             img = img / 255.0  # Normalize the image
#             print(img)
#             predict = model.predict(img)
#             predicted_class_index = np.argmax(predict)
#             print("Helllllllloooooooooo",predicted_class_index)
#             class_names = ["Good", "Bad", "Average"]  # Update with your actual class names
#             predicted_class = class_names[predicted_class_index]
#             pred=PredictionImage(
#                 user_id=request.user.id,
#                 image=img2,
#                 prediction=predicted_class
#             )
#             pred.save()
#             return render(request, "quality_check.html",{'prediction':predicted_class,'img':pred.image})
#         else:
#             print("The uploaded file is not an image.")
    
#     return render(request, "quality_check.html")


class_names_coffee = ["Dark", "Green", "Light", "Medium"]
class_names_cardamom = ["Good", "Bad", "Average"]

def predict(request):
    model_path = None  # Define model_path here, initialized as None
    class_names = None  # Initialize class_names as None

    if request.method == 'POST':
        selected_model = request.POST.get('model')

        if selected_model == "coffee":
            model_path = "models/Coffee.h5"
            class_names = class_names_coffee
        elif selected_model == "cardamom":
            model_path = "models/Cardamon_1.h5"
            class_names = class_names_cardamom

        selected_model = load_model(model_path)

        return render(request, 'upload_image.html', {'model': selected_model, 'class_names': class_names, 'model_path': model_path})

    return render(request, 'predict.html')
from PIL import Image
def upload_image(request):
    if request.method == 'POST':
        uploaded_image = request.FILES.get('image')
        model = request.POST.get('model')
        model_path = request.POST.get('model_path')  # Get model_path from the request.POST dictionary
        class_names = []
        if uploaded_image:
            # Check if the uploaded file is an image (you may want to add additional validation)
            if uploaded_image.content_type.startswith('image'):
                if model == "coffee":
                    class_names = class_names_coffee
                elif model == "cardamom":
                    class_names = class_names_cardamom

                model = load_model(model_path)

                # Load the image from the uploaded file
                img = Image.open(uploaded_image)
                img = img.resize((224, 224))  # Resize to the model's input size
                img = np.array(img)
                img = img / 255.0  # Normalize the image

                img = np.expand_dims(img, axis=0)

                predict = model.predict(img)
                predicted_class_index = np.argmax(predict)
                predicted_class = class_names[predicted_class_index]

                # Save the image to your database if needed
                pred = PredictionImage(
                    user_id=request.user.id,  # You can modify this based on your user model
                    image=uploaded_image,
                    prediction=predicted_class
                )
                pred.save()

                return render(request, 'result.html', {'predicted_class': predicted_class, 'image_url': uploaded_image.url})

    return render(request, 'upload_image.html')

def result(request):
    # Assuming you want to pass some data to the result page
    return render(request, 'result.html')
# @login_required(login_url='user_login')
# def customer_ProductView(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     # product_category = product.product_category
#     # product_subcategory = product.product_subcategory

#     # Fetch related products and reviews
#     related_products = Product.objects.filter(
#         product_category=product_category,
#         status__in=['in_stock', 'out_of_stock']
#     ).exclude(pk=product_id)[:4]

#     reviews = CustomerReview.objects.filter(product=product)

#     context = {
#         'product': product,
#         'product_category': product_category,
#         'product_subcategory': product_subcategory,
#         'related_products': related_products,
#         'reviews': reviews,
#     }

#     return render(request, 'customer_ProductView.html', context)


def sales_report(request):
    
    return render(request,'sales-report.html')



# def gifthamper(request):
import ast
#     return render(request,'gifthamper.html')
def changeDispatch(request,cart_items,order_id):
    print("FUNCTION")
    print(cart_items)
    print(order_id)
    integer_list = ast.literal_eval(cart_items)
    for cart_id in integer_list:
        cart_item = CartItem.objects.get(pk=cart_id)  
        cart_item.dispatched = True
        cart_item.save()
    order=Order.objects.get(id=order_id)
        
    order.order_status = Order.OrderStatusChoices.DISPATCHED
    order.save()
    return redirect('seller_orders')
    
def seller_orders(request):
    print("BASE VIEW")
    seller_id = request.user.id

    # Step 1: Query orders for a specific seller with successful payment status
    seller_orders = Order.objects.filter(products__seller_id=seller_id, payment_status=Order.PaymentStatusChoices.SUCCESSFUL).distinct()
      
    
        # Check if all products of the order are dispatched
    

    # Step 2: Extract relevant information from orders
    orders_data = []
    
    for order in seller_orders:
        var=CartItem.objects.filter(order_id=order.id)
        varList=[]
        for i in var:
            varList.append(i.id)
        print(varList)
        cart_items = CartItem.objects.filter(order_id=order.id) 
        order_info = {
            'order_id':order.id,
            'cart_items': varList,
            'order_date': order.order_date,
            'total_price': order.total_price,
            'items': [],
            'dispatched':order.order_status,
        }

        # Extract information about each bought item in the order
        for cart_item in CartItem.objects.filter(order=order, product__seller_id=seller_id):
            item_info = {
                'product_image': cart_item.product.image.url,
                'product_name': cart_item.product.product_name,
                'quantity': cart_item.quantity,
                'cart_item_id':cart_item.id,
                'dispatched': cart_item.dispatched,

                'total_item_price': cart_item.product.price * cart_item.quantity,  # Assuming total_item_price is product of price and quantity
            }
            order_info['items'].append(item_info)

        orders_data.append(order_info)

    # Step 3: Pass the data to the template
    context = {'orders_data': orders_data}
    
    
    
   
    
    return render(request, 'seller_orders.html', context)

# def filter_products(request):
#     if request.method == 'GET' and request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
#         # Get category and subcategory from the request
#         category = request.GET.get('category')
#         subcategory = request.GET.get('subcategory')

#         # Query the filtered products based on category and subcategory
#         filtered_products = Product.objects.filter(category=category, subcategory=subcategory)

#         # Convert the filtered products to JSON data
#         filtered_products_data = [{'product_name': product.product_name, 'price': product.price} for product in filtered_products]


#         # Return the JSON response
#         return JsonResponse({'filtered_products': filtered_products_data})
#     else:
#         # If it's not an AJAX GET request, return an error response
#         return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def createblog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        
        # Assuming you're using Django's built-in user authentication system
        author = request.user
        
        if title and content:  # Ensure title and content are provided
            new_post = BlogPost(
                title=title,
                content=content,
                image=image,
                author=author,
                created_at=timezone.now()
            )
            new_post.save()
            print("blog")
            return redirect('seller_index')  # Redirect to blog list page after successful submission
        else:
            # Handle the case where either title or content is missing
            # You may want to render a form with an error message here
            pass
    
    return render(request, 'createblog.html')

def blog(request):
    blogs = BlogPost.objects.all()  # Fetch all blogs from the database
    return render(request, 'blog.html', {'blogs': blogs})
@login_required
def farm_details(request):
    farm2=None
    farm1 = Farm.objects.filter(seller=request.user).exists()
    if farm1:
        farm2 = Farm.objects.get(seller=request.user)
    print(farm2)
    print(farm1)
    seller=request.user
    if request.method == 'POST':
        farm_name = request.POST.get('farm_name')
        location = request.POST.get('location')
        description = request.POST.get('description')
        activities = request.POST.get('activities')
        visiting_hours_from = request.POST.get('visiting_hours_from')
        visiting_hours_to = request.POST.get('visiting_hours_to')

        contact_info = request.POST.get('contact_info')
        image = request.FILES.get('image')
        if farm1:
            farm2.farm_name=farm_name
            farm2.location=location
            farm2.description=description
            farm2.activities=activities
            farm2.visiting_hours_from=visiting_hours_from
            farm2.visiting_hours_to=visiting_hours_to
            farm2.contact_info=contact_info
            farm2.image=image
            farm2.save()
            return redirect('seller_index')
        else:
            new_farm = Farm.objects.create(
            farm_name=farm_name,
            location=location,
            description=description,
            activities=activities,
            visiting_hours_from=visiting_hours_from,
            visiting_hours_to=visiting_hours_to,
            contact_info=contact_info,
            image=image,
            seller=seller,
            created_at=timezone.now()
            )
            new_farm.save()
            # return redirect('seller_index')
            
            
            
        # Save the farm details to the database
    return render(request,'farm_details.html',{'farm':farm1,'farm2':farm2})
@login_required
def farm_view(request):
    
    farms = Farm.objects.all() 
    farm_booking = SaveBooking.objects.filter(user=request.user).order_by('-id').first()

    # Fetch all blogs from the database
    return render(request, 'farm_view.html', {'farms': farms,'farm_booking': farm_booking})    
@login_required
def farm_view_details(request,farm_id):
    
    farms = Farm.objects.get(id=farm_id)  # Fetch all blogs from the database
    return render(request, 'farm_view_detail.html', {'farm': farms})  

# def farm_booking(request,farmbooking_id):
#     farm_id=Farm_Booking.objects.get(farm_id_id=farmbooking_id)
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         check_in = request.POST.get('check_in')
#         check_out = request.POST.get('check_out')
#         rooms_booked = int(request.POST.get('rooms_booked'))
#         adults = request.POST.get('adults')
#         children = request.POST.get('children')
#         check_in_con = datetime.strptime(check_in, '%Y-%m-%d')
#         check_out_con = datetime.strptime(check_out, '%Y-%m-%d')
#         # print((check_out_con - check_in_con).days)
#         diff = (check_out_con - check_in_con).days
#         print(diff)
#         # Calculate the difference in days
#         # date_difference = (check_out_con - check_in_con).days        
        

#         # Check if rooms are available
#         farm_booking = Farm_Booking.objects.get(farm_id_id=farmbooking_id)
#         if int(farm_booking.rooms) >= rooms_booked:
#             # Calculate total price
#             total_price = farm_booking.price * rooms_booked*diff

#             # Create SaveBooking object and save it
#             save_booking = SaveBooking.objects.create(
#                 farm_id=farm_id.id,
#                 name=name,
#                 check_in=check_in,
#                 check_out=check_out,
#                 rooms_booked=rooms_booked,
#                 adults=adults,
#                 children=children,
#                 total_price=total_price
#             )
#             save_booking.save()
            
            
#             farm_booking.rooms = str(int(farm_booking.rooms) - rooms_booked)  # Convert to integer, subtract, and then convert back to string
#             farm_booking.save()
#             messages.success(request, 'Your booking has been saved successfully!')
#             total_price_float = float(total_price)  
#             client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

#         # Create a new order
#             order_data = {
#                 'amount': int(total_price_float*100),  # Amount should be in paisa
#                 'currency': 'INR',
#                 'receipt': str(save_booking.id),  # Use booking ID as receipt ID
#                 'payment_capture': 1  # Auto capture payment
#             }
#             order = client.order.create(data=order_data)

#         # Redirect the user to the Razorpay checkout page
#             return render(request, 'payment.html', {'order': order})
#             # return redirect('index')  # Replace 'success_url' with the URL name of the success page
#         else:
#             messages.error(request, 'Sorry, the selected number of rooms is not available.')
#             return redirect('farm_booking')  # Redirect back to the booking page
#     else:
#         # Handle GET request if needed
#         return render(request, 'farm_booking.html')
# #  return render(request, 'farm_booking.html')

# razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
       
        

    
    
    
    
    
    
    
    
razorpay_client = razorpay.Client(
 	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def farm_booking(request, farmbooking_id):
    farm_booking = get_object_or_404(Farm_Booking, farm_id=farmbooking_id)
    name = request.user

    if request.method == 'POST':
        name = request.POST.get('name')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        rooms_booked = int(request.POST.get('rooms_booked'))
        adults = request.POST.get('adults')
        children = request.POST.get('children')
        phone_no=request.POST.get('phone_no')

        check_in_con = datetime.strptime(check_in, '%Y-%m-%d')
        check_out_con = datetime.strptime(check_out, '%Y-%m-%d')
        diff = (check_out_con - check_in_con).days
        

        total_price = farm_booking.price * rooms_booked * diff

        save_booking = SaveBooking.objects.create(
            farm=farm_booking,
            name=name,
            phone_no=phone_no,
            check_in=check_in,
            check_out=check_out,
            rooms_booked=rooms_booked,
            adults=adults,
            children=children,
            total_price=total_price
        )
        save_booking.save()

        farm_booking.rooms = str(int(farm_booking.rooms) - rooms_booked)  
        farm_booking.save()
        amount=int(total_price*100)
        new_amt=amount/100
        
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                        currency='INR',
                                                        payment_capture='0'))
    
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = 'http://127.0.0.1:8000/process_payment/'+str(save_booking.id)+'/'+str(amount)+'/'
        
            # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = 'INR'
        context['callback_url'] = callback_url
        
        
        

        return render(request, 'payment.html', {'order': razorpay_order,'razorpay_merchant_key':settings.RAZOR_KEY_ID,'razorpay_amount':amount,'callback_url':callback_url,'booking_id': save_booking.id,'new_amt':new_amt})
    
    return render(request, 'farm_booking.html', {'farm_booking': farm_booking,'name':name})
from twilio.rest import Client

@csrf_exempt
def process_payment(request,booking_id,amount):
    print('capture')
    print(booking_id,amount)
    if request.method == 'POST':
        # payment_id = request.POST.get('razorpay_payment_id')
        # razorpay_order_id = request.POST.get('razorpay_order_id')
        # signature = request.POST.get('razorpay_signature')
        # print(payment_id,razorpay_order_id,signature)
        # params_dict = {
        #     'razorpay_order_id': razorpay_order_id,
        #     'razorpay_payment_id': payment_id,
        #     'razorpay_signature': signature
        # }
 
        #     # verify the payment signature.
        # result = razorpay_client.utility.verify_payment_signature(
        #         params_dict)
        # if result is not None:
        #     razorpay_client.payment.capture(payment_id, amount)
        booking = get_object_or_404(SaveBooking, id=booking_id)
        check_in_date = booking.check_in.strftime("%Y-%m-%d")  # Format date as needed
        check_out_date = booking.check_out.strftime("%Y-%m-%d")  # Format date as needed
        stay_name = booking.farm.stay_name
        message_body = f"🏡 Your booking for {stay_name} 🏨 from {check_in_date} 📅 to {check_out_date} 📅 is successful. Thank you for choosing our service! 🎉"

        print(booking_id)
        booking.status = "success"
        booking.save()
        
        client = Client("AC72d0d232baf2a2fba6788361351e6a46", "6e9f1f907246740d18f121972c80aec7")

        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=message_body,
            to='whatsapp:+917510284058'  # Replace with the user's WhatsApp number
        )
        messages.success(request, 'Payment successful!')
        return render(request, 'index.html')
            # messages.error(request, 'Payment verification failed!')
            # return render(request, 'farm_booking.html')
    else:
        return redirect('index')
def seller_booking(request,farm_id):
    
    if request.method == 'POST':
       stay_name=request.POST.get('stay_name')
       rooms=request.POST.get('rooms') 
       price=request.POST.get('price')
       if stay_name and price:
            stay = Farm_Booking(
                stay_name=stay_name,
                rooms=rooms,
                price=price,
                farm_id_id=farm_id,
            )
            stay.save()
            print('fkjj')
            return redirect('seller_index')
            
           
    return render(request,'booking_seller.html')


from django.utils.timezone import now

def booking_result_display(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    # Get the current date
    current_date = datetime.now().date()

    # Query bookings made by the user with check-in date greater than current date
    user_bookings = SaveBooking.objects.filter(user=user, check_in__gt=current_date, status='success')

    return render(request, 'booking_result_display.html', {'user_bookings': user_bookings, 'current_date': current_date})


def seller_report(request):
    return render(request, 'seller_report.html')
from django.http import HttpResponse, HttpResponseNotAllowed
from django.template.loader import get_template

# def generate_sales_report(request):
#     if request.method == 'POST':
#         start_date = request.POST.get('start_date')
#         end_date = request.POST.get('end_date')

#         # Convert start_date and end_date to datetime objects
#         # Assuming start_date and end_date are in the format 'YYYY-MM-DD'
#         start_datetime = timezone.make_aware(timezone.datetime.strptime(start_date, '%Y-%m-%d'))
#         end_datetime = timezone.make_aware(timezone.datetime.strptime(end_date, '%Y-%m-%d'))


#         # Filter orders based on the selected date range
#         orders = Order.objects.filter(order_date__range=[start_datetime, end_datetime])

#         # Generate PDF
#         template_path = 'seller_salesreport.html'
#         context = {'orders': orders}
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = 'filename="sales_report.pdf"'

#         template = get_template(template_path)
#         html = template.render(context)

#         # Create PDF
#         pisa_status = pisa.CreatePDF(html, dest=response)
#         if pisa_status.err:
#             return HttpResponse('Error creating PDF', status=500)
#         return response
#     else:
#         # Handle GET request or other methods if needed
#         return HttpResponseNotAllowed(['POST'])



def generate_sales_report(request,):
    seller=request.user.id
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Convert start_date and end_date to datetime objects with timezone information
        start_datetime = timezone.make_aware(timezone.datetime.strptime(start_date, '%Y-%m-%d'))
        end_datetime = timezone.make_aware(timezone.datetime.strptime(end_date, '%Y-%m-%d'))

        # Filter orders based on the selected date range
        orders = Order.objects.filter(Q(order_date__range=[start_datetime, end_datetime]) &
    Q(products__seller_id=seller))

        # Initialize a dictionary to store sales data
        sales_data = {}

        # Iterate over each order
        for order in orders:
            # Get all cart items associated with the order
            cart_items = CartItem.objects.filter(order=order)

            # Iterate over each cart item
            for cart_item in cart_items:
                product = cart_item.product

                # Check if the product is already in sales_data
                if product.id not in sales_data:
                    sales_data[product.id] = {
                        'order_date': order.order_date,
                        'product_name': product.product_name,
                        'total_quantity': cart_item.quantity,
                        'total_sales': cart_item.quantity * product.price
                    }
                else:
                    # Update total_quantity and total_sales
                    sales_data[product.id]['total_quantity'] += cart_item.quantity
                    sales_data[product.id]['total_sales'] += cart_item.quantity * product.price

        # You can now use sales_data to generate the sales report

        # For demonstration purposes, let's print the sales data
        for product_id, data in sales_data.items():
            print(f"Product: {data['product_name']}, Total Quantity Sold: {data['total_quantity']}, Total Sales: {data['total_sales']}")

        # Once you have the sales data, you can proceed to generate the PDF report

        # Generate PDF
        template_path = 'seller_salesreport.html'
        context = {'sales_data': sales_data}
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="sales_report.pdf"'

        template = get_template(template_path)
        html = template.render(context)

        # Create PDF
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('Error creating PDF', status=500)
        return response
    else:
        # Handle GET request or other methods if needed
        return HttpResponseNotAllowed(['POST'])

def seller_sales_report(request):
    return render(request, 'seller_salesreport.html')

from django.db.models import Sum

# Assuming you want to recommend the top 5 most sold products
def get_most_sold_products(num_recommendations=5):
    # Aggregate total quantity sold for each product
    sold_products = CartItem.objects.filter(order__payment_status=Order.PaymentStatusChoices.SUCCESSFUL)\
                                     .values('product__id', 'product__product_name')\
                                     .annotate(total_quantity_sold=Sum('quantity'))\
                                     .order_by('-total_quantity_sold')[:num_recommendations]

    # Extract product IDs and names from the query results
    product_ids = [item['product__id'] for item in sold_products]
    product_names = [item['product__product_name'] for item in sold_products]

    # Return product IDs and names
    return product_ids, product_names




def seller_booking_display(request):
    seller = request.user

    # Retrieve the farm associated with the seller
    farm = Farm.objects.get(seller=seller)

    # Retrieve all SaveBooking instances associated with the farm
    bookings_data = SaveBooking.objects.filter(farm__farm_id=farm.id)

    context = {
        'seller': seller,
        'farm': farm,
        'bookings_data': bookings_data,
    }
    print(bookings_data)

    return render(request, 'seller_booking_display.html', context)

def booking_notification(seller_id, farm_id):
    try:
        # Retrieve the farm associated with the booking
        farm = Farm.objects.get(id=farm_id)

        # Assuming you have a list of bookings for the farm
        bookings = SaveBooking.objects.filter(farm__farm_id=farm_id, status='success')

        # Create a notification for the seller for each successful booking associated with the farm
        for booking in bookings:
            notification = Notification(
                seller_id=seller_id,
                message=f"A booking for the farm {farm.farm_name} has been successfully made by {booking.name}."
            )
            notification.save()
    except Farm.DoesNotExist:
        # Handle the case where the farm does not exist
        print("Farm does not exist")
    except SaveBooking.DoesNotExist:
        # Handle the case where there are no successful bookings for the farm
        print("No successful bookings for the farm")
        
from django.shortcuts import redirect, get_object_or_404
# 

def cancel_booking(request, booking_id):
    booking = get_object_or_404(SaveBooking, id=booking_id)
    check_in_date = booking.check_in.strftime("%Y-%m-%d")  # Format date as needed
    check_out_date = booking.check_out.strftime("%Y-%m-%d")  # Format date as needed
    stay_name = booking.farm.stay_name    
    # Update the booking status to canceled
    num_rooms_booked = booking.rooms_booked
    
    # Retrieve the corresponding farm booking
    farm_booking = booking.farm
    
    # Increment the available rooms
    farm_booking.rooms = str(int(farm_booking.rooms) + num_rooms_booked)
    farm_booking.save()
    
    # Update the booking status to canceled
    message_body = f"❌ Your booking for {stay_name} 🏨 from {check_in_date} 📅 to {check_out_date} 📅 has been canceled. We apologize for any inconvenience caused."

    # Update booking status to "Canceled"
    booking.status = "Canceled"
    booking.save()

    # Send cancellation message via Twilio WhatsApp
    client = Client("AC72d0d232baf2a2fba6788361351e6a46", "6e9f1f907246740d18f121972c80aec7")
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=message_body,
        to='whatsapp:+917510284058'  # Replace with the user's WhatsApp number
    )
        
        # Set rooms_updated to True
    booking.rooms_updated = True
    
    # Save the changes
    booking.save()
    
    # Add a success message
    # messages.success(request, 'Booking has been successfully canceled.')

    # Redirect to the booking display page
    return redirect('booking_result_display', user_id=request.user.id)
def update_available_rooms(request):
    # Get bookings with exceeded checkout dates, status is 'successful', and rooms have not been updated yet
    expired_bookings = SaveBooking.objects.filter(
        check_out__lt=timezone.now(),
        rooms_updated=False  
    )
    
    for booking in expired_bookings:
        farm_booking = booking.farm
        farm_booking.rooms = str(int(farm_booking.rooms) + booking.rooms_booked)
        farm_booking.save()
        
        # Set the rooms_updated flag to True
        booking.rooms_updated = True
        booking.save()
    
    # Optionally, you can redirect to a specific page after updating available rooms
    return redirect('index') 


def hub_home(request):
    
    return render(request,'hub_home.html')


from django.contrib.auth import authenticate, login as auth_login

@never_cache
def hub_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if email and password:
            user = authenticate(request, email=email, password=password)
            if user is not None:

                auth_login(request, user)  
              
                if user.hub_status:
                    print("hubstatus")
                    return redirect('hub_home')  # Redirect to customer index page
                
            else:
                error_message = "Invalid login credentials."
                return render(request, 'hub_login.html', {'error_message': error_message})
        # else:
        #     error_message = "Please fill out all fields."
        #     return render(request, 'Login.html', {'error_message': error_message})
    return render(request,'hub_login.html')



def hub_orders(request): 
    
    
    
    hub_orders = Order.objects.filter(order_status="Dispatched").distinct()
      
        # Check if all products of the order are dispatched
    print(hub_orders)

    # Step 2: Extract relevant information from orders
    orders_data = []
    
    for order in hub_orders:
        var=CartItem.objects.filter(order_id=order.id)
        varList=[]
        for i in var:
            varList.append(i.id)
        print(varList)
        order_info = {
            'order_id':order.id,
            'cart_items': varList,
            'order_date': order.order_date,
            'total_price': order.total_price,
            'items': [],
            'accepted_by_store':order.accepted_by_store,
        }

        # Extract information about each bought item in the order
        for cart_item in CartItem.objects.filter(order=order):
            item_info = {
                'product_image': cart_item.product.image.url,
                'product_name': cart_item.product.product_name,
                'quantity': cart_item.quantity,
                'cart_item_id':cart_item.id,
                'accepted_by_store': cart_item.accepted_by_store,

                'total_item_price': cart_item.product.price * cart_item.quantity,  # Assuming total_item_price is product of price and quantity
            }
            order_info['items'].append(item_info)

        orders_data.append(order_info)

    # Step 3: Pass the data to the template
    context = {'orders_data': orders_data}
    
    
    
    
    
    
    
    
    
    
    
    
    

    return render(request, 'hub_orders.html',context)

def changeStore(request, cart_items, order_id):
    integer_list = ast.literal_eval(cart_items)

    for cart_id in integer_list:
        cart_item = CartItem.objects.get(pk=cart_id)
        print(cart_item)
        cart_item.accepted_by_store = True
        cart_item.save()

    order = Order.objects.get(id=order_id)
    order.accepted_by_store = True
    order.save()

    return redirect('hub_orders')






    # dispatched_order_ids = CartItem.objects.filter(dispatched=True).values('order_id').distinct()

    # # Retrieve orders corresponding to the dispatched cart items
    # orders = Order.objects.filter(id__in=dispatched_order_ids)

    # if request.method == 'POST':
    #     cart_item_id = request.POST.get('cart_item_id')
    #     cart_item = CartItem.objects.get(pk=cart_item_id)
    #     cart_item.accepted_by_store = True
    #     cart_item.save()

    #     # Check if all cart items in the order are dispatched
    #     order = cart_item.order
    #     if order and all(item.dispatched for item in order.cartitem_set.all()):
    #         order.accepted_by_store = True
    #         order.save()

        # return redirect('hub_orders')
        
        
        
        
        
        
from django.contrib.auth import get_user_model
 
def delivery_registration(request):
    if request.method == 'POST':
        # Extract data from the request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        vehicle_type = request.POST.get('vehicle_type')
        license_number = request.POST.get('license_number')
        locality = request.POST.get('locality')
        
        # Save data to CustomUser model
        # User = get_user_model()
        user = CustomUser(email=email, password=password, first_name=first_name, last_name=last_name, is_delivery=True, is_active=False)
        user.save()

        # Save data to DeliveryAgent model
        delivery_agent = DeliveryAgent.objects.create(
            phone_number=phone_number,
            vehicle_type=vehicle_type,
            license_number=license_number,
            password=password,
            locality=locality
        )
        # Save the delivery_agent object
        delivery_agent.save()
        # Redirect to success page or wherever you want
        return redirect('index')

    return render(request, 'delivery_registration.html')
def delivery_agent_home(request):
    return render(request,'delivery_agent_home.html')
def delivery_agent_profile(request):
    print("save buttonnn clicked")

    delivery_agent, created = DeliveryAgent.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        print("save clicked")
        # Get the form data from the POST request
        locality = request.POST.get('locality')
        phone_number = request.POST.get('phone_number')
        license_number = request.POST.get('license_number')
        
        # Update the attributes of the delivery agent
        delivery_agent.locality = locality
        delivery_agent.phone_number = phone_number
        delivery_agent.license_number = license_number
        
        # Save the changes to the delivery agent
        delivery_agent.save()
        print(delivery_agent)
    context = {
        'delivery_agent': delivery_agent,
        # 'form_submitted': request.method == 'POST',
    }
    
    return render(request, 'delivery_agent_profile.html', context)

# def update_delivery_profile(request):
#     delivery_agent, created = DeliveryAgent.objects.get_or_create(user=request.user)
#     if request.method == 'POST':
#         # Get the form data from the POST request
#         locality = request.POST.get('locality')
#         phone_number = request.POST.get('phone_number')
#         license_number = request.POST.get('license_number')
        
#         # Update the attributes of the delivery agent
#         delivery_agent.locality = locality
#         delivery_agent.phone_number = phone_number
#         delivery_agent.license_number = license_number
        
#         # Save the changes to the delivery agent
#         delivery_agent.save()
        
#     context = {
#         'form_submitted': request.method == 'POST',
#     }
#     return render(request, 'delivery_agent_profile.html', context)

def address_card(request):
    addresses = Address.objects.filter(user=request.user)  
    
    return render(request,"address_card.html",{'addresses': addresses})

def add_address(request):
    
    if request.method == 'POST':
        house_building = request.POST.get('house_building')
        road_area_colony = request.POST.get('road_area_colony')
        city = request.POST.get('city')
        district = request.POST.get('district')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phone')

        # Validate form data (you can add more validation as needed)

        # Create and save Address instance
        address = Address.objects.create(
            user=request.user,  # Assuming the user is authenticated
            house_building=house_building,
            road_area_colony=road_area_colony,
            city=city,
            district=district,
            pincode=pincode,
            phone=phone
        )
        return redirect('address_card')  # Redirect to address list view

    return render(request, 'add_address.html')