from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from .models import UserProfile
from .forms import ProductForm
from .models import Product
from django.shortcuts import render, get_object_or_404

def index(request):
    return render(request,'index.html')

def seller_index(request):
    return render(request,'sellerhome.html')

def cust_profile(request,user):
    print(user)
    data=UserProfile.objects.filter(user_id=user)
    return render(request,'custprofile.html',{'data':data})



def shop(request):
    # Get products added by the suppliers
    supplier_products = Product.objects.all()  # You can add filters if needed
    
    context = {
        'supplier_products': supplier_products
    }
    return render(request, 'shop.html', context)

# views.py


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'shop-single.html', {'product': product})


# @login_required
# def profile(request):
#     user_profile, created = UserProfile.objects.get_or_create(user=request.user)

#     if request.method == 'POST':
#         action = request.POST.get('action')
        
#         if action == 'submit':
#             # print("Entered")
#             # Update the user profile with form data
#             user_profile.f_name = request.POST.get('fName')
#             user_profile.email = request.POST.get('email')
#             user_profile.phone = request.POST.get('phone')
#             user_profile.l_name = request.POST.get('sName')
#             user_profile.street = request.POST.get('street')
#             user_profile.city = request.POST.get('city')
#             user_profile.state = request.POST.get('state')
#             user_profile.zip_code = request.POST.get('zip_code')
#             profile_picture = request.FILES.get('profilePicture')

#             if profile_picture:
#                 user_profile.profile_picture = profile_picture

#             user_profile.save()
#             messages.success(request, 'Profile created successfully!')

#             # Redirect to the same page to display the user profile update form
#             return redirect('profile')
#         elif action == 'update':
#             # if request.user.email == request.POST.get('email'):
#                 user_profile.f_name = request.POST.get('fName')
#                 user_profile.email = request.user.email 
#                 user_profile.phone = request.POST.get('phone')
#                 user_profile.l_name = request.POST.get('sName')
#                 user_profile.street = request.POST.get('street')
#                 user_profile.city = request.POST.get('city')
#                 user_profile.state = request.POST.get('state')
#                 user_profile.zip_code = request.POST.get('zip_code')
#                 profile_picture = request.FILES.get('profilePicture')

#                 if profile_picture:
#                     user_profile.profile_picture = profile_picture

#                 user_profile.save()
#                 messages.success(request, 'Profile updated successfully!')

#     context = {
#         'user_profile': user_profile
#     }
    
#     def __str__(self):
#         return self.user.username
#     return render(request, 'custprofile.html', context)

@login_required
def profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'submit':
            # Update the user profile with form data
            user_profile.f_name = request.POST.get('fName')
            user_profile.email = request.user.email  # Use the logged-in user's email
            user_profile.phone = request.POST.get('phone')
            user_profile.l_name = request.POST.get('sName')
            user_profile.street = request.POST.get('street')
            user_profile.city = request.POST.get('city')
            user_profile.state = request.POST.get('state')
            user_profile.zip_code = request.POST.get('zip_code')
            profile_picture = request.FILES.get('profilePicture')

            if profile_picture:
                user_profile.profile_picture = profile_picture

            user_profile.save()
            messages.success(request, 'Profile created/updated successfully!')

    context = {
        'user_profile': user_profile
    }

    return render(request, 'custprofile.html', context)



def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to a page showing the list of products
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})





