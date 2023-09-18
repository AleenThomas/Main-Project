from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from .models import Customer_Profile
from .forms import ProductForm
from .models import Product,CustomUser,SellerDetails,Wishlist,CartItem
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from .models import CustomUser, SellerDetails
from django.db.models import Q
from django.core.paginator import Paginator



def index(request):
    
    user=request.user
    if user.is_anonymous:
        return render(request,'index.html')
    elif user.is_seller==True:
        return redirect('seller_index')
    else:
        
        return render(request,'index.html')
    # return render(request,'index.html')
    
def contact(request):
    return render(request,'contact.html')
# def reg_step(request):
#     return render(request,'reg_step.html')


def wishlist_view(request):
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.get_or_create(user=request.user)[0]
        wishlist_products = wishlist.products.all()
        return render(request, 'wishlist.html', {'wishlist_products': wishlist_products})
    else:
        return render(request, 'login_required.html')

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    return JsonResponse({'message': 'Product added to wishlist'})

@login_required
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





def seller_reg_step(request):
    if request.method == 'POST':
        step = request.POST.get('step')

        print(step)
        # Check which step the form data is coming from
        if step == '1':
            print("one")
            # Step 1 Data
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            gstn = request.POST.get('gstn')

            # Check for existing user with the same email
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
            else:
                # Create a new user and set the password
                user = CustomUser(name=name, email=email, gstn=gstn)
                user.password = make_password(password)  # Hash the password
                user.is_seller = True  # Mark as a seller
                user.save()

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





# Import the necessary models


# ...

# def seller_reg_step(request):
#     if request.method == 'POST':
#         step = request.POST.get('step')
        
#         if step == '1':
#             # Step 1 Data
#             name = request.POST.get('name')
#             email = request.POST.get('email')
#             password = request.POST.get('password')
#             gstn = request.POST.get('gstn')

#             if CustomUser.objects.filter(email=email).exists():
#                 messages.error(request, "Email already exists.")
#             else:
#                 user = CustomUser(name=name, email=email, gstn=gstn)
#                 user.password = make_password(password)
#                 user.is_seller = True
#                 user.save()

#                 request.session['user_id'] = user.id

#                 messages.success(request, "Step 1 completed successfully.")
#                 return redirect('reg_step')

#         elif step == '2':
#             # Step 2 Data
#             user_id = request.session.get('user_id')
#             if user_id:
#                 user = CustomUser.objects.get(id=user_id)
                
#                 store_name = request.POST.get('store-name')
#                 phone_number = request.POST.get('phone-number')
#                 pincode = request.POST.get('pincode')
#                 pickup_address = request.POST.get('pickup-address')
#                 city = request.POST.get('city')
#                 state = request.POST.get('state')

#                 seller_details = user.seller_details_user.all().first()

#                 if not seller_details:
#                     seller_details = SellerDetails(
#                         user=user,
#                         store_name=store_name,
#                         phone_number=phone_number,
#                         pincode=pincode,
#                         pickup_address=pickup_address,
#                         city=city,
#                         state=state
#                     )
#                     seller_details.save()
#                 else:
#                     seller_details.store_name = store_name
#                     seller_details.phone_number = phone_number
#                     seller_details.pincode = pincode
#                     seller_details.pickup_address = pickup_address
#                     seller_details.city = city
#                     seller_details.state = state
#                     seller_details.save()

#                 messages.success(request, "Step 2 completed successfully.")
#                 return redirect('reg_step')

#         elif step == '3':
#             # Step 3 Data
#             user_id = request.session.get('user_id')
#             if user_id:
#                 user = CustomUser.objects.get(id=user_id)
                
#                 account_holder_name = request.POST.get('account-holder-name')
#                 account_number = request.POST.get('account-number')
#                 bank_name = request.POST.get('bank-name')
#                 branch = request.POST.get('branch')
#                 ifsc_code = request.POST.get('ifsc-code')

#                 seller_details = user.seller_details_user.all().first()

#                 if not seller_details:
#                     seller_details = SellerDetails(
#                         user=user,
#                         account_holder_name=account_holder_name,
#                         account_number=account_number,
#                         bank_name=bank_name,
#                         branch=branch,
#                         ifsc_code=ifsc_code
#                     )
#                     seller_details.save()
#                 else:
#                     seller_details.account_holder_name = account_holder_name
#                     seller_details.account_number = account_number
#                     seller_details.bank_name = bank_name
#                     seller_details.branch = branch
#                     seller_details.ifsc_code = ifsc_code
#                     seller_details.save()

#                 messages.success(request, "Step 3 completed successfully.")
#                 # Redirect to confirmation page or other steps
#                 return redirect('seller_reg_step')

#     return render(request, 'reg_step.html')











def seller_index(request):
    return render(request,'sellerhome.html')


    
def shop(request):
    # Get products added by the suppliers
    supplier_products = Product.objects.all()  # You can add filters if needed
    paginator = Paginator(supplier_products, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'supplier_products': supplier_products,
        'page':page
    }
    return render(request, 'shop.html', context)

# @login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'shop-single.html', {'product': product})



@login_required(login_url='custom_login')
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







@login_required(login_url='custom_login')  # Redirects to the login page if not logged in
def add_product(request):
    if request.user.is_seller:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.save(commit=False)
                product.seller = request.user  # Assign the logged-in seller to the product
                product.save()
                return redirect('index')  # Redirect to a page showing the list of products
        else:
            form = ProductForm()

        return render(request, 'add_product.html', {'form': form})
    else:
        # If the logged-in user is not a seller, you can redirect them or show an error message
        # For example, you can redirect them to a page where they can register as a seller
        return redirect('seller_register') 




# def update(request,update_id):
#     task=Product.objects.get(id=update_id) 
#     form=create_form(request.POST or None,instance=task) 
#     if form.is_valid():
#         form.save()
#         return redirect('table')
#     return render(request,'update.html',{'form':form})






@login_required(login_url='custom_login')
def customer_Profile(request):
    user_profile, created = Customer_Profile.objects.get_or_create(customer=request.user)

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


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product_id=product.id)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('shop')

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
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
    cart_item.delete()
    return redirect('cart')

# def update_cart(request):
#     if request.method == 'POST':
#         cart_item_id = request.POST.get('cart_item_id')
#         action = request.POST.get('action')

#         try:
#             cart_item = CartItem.objects.get(id=cart_item_id)

#             if action == 'increase':
#                 cart_item.quantity += 1
#                 cart_item.save()
#             elif action == 'decrease':
#                 if cart_item.quantity > 1:
#                     cart_item.quantity -= 1
#                     cart_item.save()
#                 else:
#                     cart_item.delete()
#                     messages.info(request, "Item removed from the cart.")

#         except CartItem.DoesNotExist:
#             messages.warning(request, "Item does not exist in the cart.")
    
#     return redirect('cart')  # Redirect back to t


def decrease_item(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
    except CartItem.DoesNotExist:
        pass  # Handle the case when the item does not exist in the cart
    return redirect('cart')  # Redirect back to the cart page after decreasing the item quantity

def increase_item(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        pass  # Handle the case when the item does not exist in the cart
    return redirect('cart')


def search(request):
    query = request.GET.get('q')
    if query:
        results = Product.objects.filter(product_name__icontains=query)
    else:
        results = []

    return render(request, 'search_results.html', {'results': results})




# -------------------------------------------------admin---------------------------------------------------
def index_admin(request):
    return render(request,'admin\indexadmin.html')


def search_product(request,name):
    print(name)

    # Perform the search using a Q object to filter the Product model
    results = Product.objects.filter(
        Q(product_name__icontains=name) | Q(description__icontains=name)
    )
    print(results)

    # Serialize the results to JSON
    serialized_results = [{'id': product.id, 'name': product.product_name,'image':product.image.url} for product in results]
    
    return JsonResponse({'results': serialized_results})