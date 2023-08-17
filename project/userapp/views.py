from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from.models import CustomUser
from django.contrib.auth import authenticate, login as auth_login
# Create your views here.
def customer_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role', None)
        
        if email and password and role:
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
                return redirect('login')
            
            user = CustomUser(name=name, email=email)
            user.set_password(password)
            
            if role == 'customer':
                user.is_customer = True
            user.save()
            messages.success(request, "Registered as a customer successfully")
            return redirect('/')  # Redirect to homepage or thank-you page
        
        else:
            messages.error(request, "Missing required fields")
    
    return render(request, 'register.html')




def seller_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role', None)
        
        if email and password and role:
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
                return redirect('seller_register')
            
            user = CustomUser(name=name, email=email)
            user.set_password(password)
            
            if role == 'seller':
                user.is_seller = True
            user.save()
            messages.success(request, "Registered as a seller successfully")
            return redirect('/')  # Redirect to homepage or thank-you page
        
        else:
            messages.error(request, "Missing required fields")
    
    return render(request, 'sellerreg.html')








def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user)                
                return redirect('/')  
            else:
                error_message = "Invalid login credentials."
                return render(request, 'login.html', {'error_message': error_message})
        # else:
        #     error_message = "Please fill out all fields."
        #     return render(request, 'Login.html', {'error_message': error_message})
    return render(request,'login.html')
def logout(request):
    auth.logout(request)
    return redirect('/')

