from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
def index(request):
    return render(request,'index.html')

def cust_profile(request):
    return render(request,'custprofile.html')



# @login_required
# def profile(request):
#     user_profile, created = UserProfile.objects.get_or_create(user=request.user)

#     if request.method == 'POST':
#         action = request.POST.get('action')
        
#         if action == 'submit':
#             # Update the user profile with form data
#             user_profile.full_name = request.POST.get('fullName')
#             user_profile.email = request.POST.get('email')
#             user_profile.phone = request.POST.get('phone')
#             user_profile.password = request.POST.get('password')
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
#             # Update the user profile with updated form data
#             user_profile.full_name = request.POST.get('fullName')
#             user_profile.email = request.POST.get('email')
#             user_profile.phone = request.POST.get('phone')
#             user_profile.password = request.POST.get('password')
#             user_profile.street = request.POST.get('street')
#             user_profile.city = request.POST.get('city')
#             user_profile.state = request.POST.get('state')
#             user_profile.zip_code = request.POST.get('zip_code')
#             profile_picture = request.FILES.get('profilePicture')

#             if profile_picture:
#                 user_profile.profile_picture = profile_picture

#             user_profile.save()
#             messages.success(request, 'Profile updated successfully!')

#     context = {
#         'user_profile': user_profile
#     }
    
#     def __str__(self):
#         return self.user.username
#     return render(request, 'custprofile.html', context)

