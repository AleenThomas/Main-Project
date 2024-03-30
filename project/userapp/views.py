from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from.models import CustomUser
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.views.decorators.cache import never_cache

# from storeapp.models import UserProfile
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
            user.is_active = False
            user.save()
           
          
          
            print("message")

            # Generate a verification token
            token = default_token_generator.make_token(user)

            # Create the verification URL with the token
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            verification_url = reverse('email_verification', args=[uidb64, token])

            # Construct the email message with the verification URL
            message = f"Click the following link to verify your email: {request.build_absolute_uri(verification_url)}"

            # Send the verification email
            send_mail(
                'Email Verification',
                message,
                'grovegusto@gmail.com',  # Replace with your sender email
                [user.email],
                fail_silently=False,
            )

            messages.success(request, "Registration successful! Please check your email to verify your account.")
        else:
            messages.error(request, "Registration failed. Please try again.")
    return render(request, 'custreg.html')
           
    #         messages.success(request, "Registered as a customer successfully")
    #         return redirect('custom_login')  # Redirect to homepage or thank-you page
        
    #     else:
    #         messages.error(request, "Missing required fields")
    
    # return render(request, 'custreg.html')




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







@never_cache
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
                    low_stock_notification_url = reverse('low_stock_notification', args=[user.id])
                    return redirect(low_stock_notification_url)
                elif user.is_delivery:
                    return redirect('delivery_agent_home')
                elif user.is_superuser:
                    return redirect('admin_home')
                
                
                    
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

def email_verification(request, uidb64, token):
    User = get_user_model()

    try:
        user_id = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=user_id)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Email verification successful! You can now log in.")
        else:
            messages.error(request, "Email verification failed. Please request a new verification email.")
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    return redirect('custom_login')