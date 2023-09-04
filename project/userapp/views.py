from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from.models import CustomUser
from storeapp.models import UserProfile
from django.contrib.auth import authenticate, login as auth_login
# Create your views here.
def customer_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # role = request.POST.get('role', None)
        confirm_password=request.POST.get('password-repeat')
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request,"email already exits")
        elif password!=confirm_password:
            messages.error(request,"password not match")

        elif email and password:
            user = CustomUser(name=name, email=email)
            user.set_password(password)
            user.is_customer = True
            # if role == 'customer':
            #     user.is_customer = True
            user.save()
           
            messages.success(request, "Registered as a customer successfully")
            return redirect('custom_login')  # Redirect to homepage or thank-you page
        
        else:
            messages.error(request, "Missing required fields")
    
    return render(request, 'custreg.html')




def seller_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password=request.POST.get('password-repeat')
        gstn = request.POST.get('gstn') 

        # role = request.POST.get('role', None)
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request,"email already exits")
        elif password!=confirm_password:
            messages.error(request,"password not match")
        elif not gstn:
            messages.error(request, "GSTN field is required")
        elif email and password:
            # if CustomUser.objects.filter(email=email).exists():
            #     messages.error(request, "Email already exists")
            #     return redirect('seller_register')
            
            user = CustomUser(name=name, email=email,gstn=gstn)
            user.set_password(password)
            user.is_seller = True
            # if role == 'seller':
            #     user.is_seller = True
            user.save()
            messages.success(request, "Registered as a seller successfully")
            return redirect('/')  # Redirect to homepage or thank-you page
        
        else:
            messages.error(request, "Missing required fields")
    
    return render(request, 'sellerreg.html')








def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user)                
                if user.is_customer:
                    return redirect('index')  # Redirect to customer index page
                elif user.is_seller:
                    return redirect('seller_index') 
            else:
                error_message = "Invalid login credentials."
                return render(request, 'custlogin.html', {'error_message': error_message})
        # else:
        #     error_message = "Please fill out all fields."
        #     return render(request, 'Login.html', {'error_message': error_message})
    return render(request,'custlogin.html')
def logout(request):
    auth.logout(request)
    return redirect('/')

