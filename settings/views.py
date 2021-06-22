from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
import imghdr
from imghdr import tests
from django.contrib.auth.decorators import login_required
from validate_email import validate_email
from django.views import View
import json
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.contrib.auth import logout as django_logout

from .forms import EditForm, PasswordChangingForm
from account.utils import validate_image
from authentication.utils import username_validation
from account.models import Profile
from account.decorators import check_ban

# Create your views here.
@check_ban
def index(request):
    return redirect('edit')

@check_ban
@login_required(login_url='/authentication/login/')
def edit(request):
    profile = Profile.objects.get(user=request.user)
    user = profile.user 

    username = user.username
    description = profile.description
    profile_pic = profile.image

    if request.method == 'POST':
        everything_ok = True
        error_msg = ''

        image = request.FILES.get('imageField', False)
        username = request.POST['username']
        description = request.POST['description']
    
        # Username validation
        validated_username = username_validation(request, username, everything_ok, error_msg)
        everything_ok = validated_username['everything_ok']
        error_msg = validated_username['error_msg']

        # Description validation
        if len(description) > 300:
            everything_ok = False
            error_msg = 'Description must be less than 300 characters.'

        # Image validation
        if image:
            validated_image = validate_image(image, everything_ok, error_msg)
            everything_ok = validated_image['everything_ok']
            error_msg = validated_image['error_msg']

        if everything_ok:
            user.username = username 
            user.save()

            if image:
                profile.image = image 
                profile_pic = profile.image
            
            profile.description = description
            profile.save()

            messages.success(request, 'Profile updated.')  
        else:
            messages.error(request, error_msg)  

    context = {
        'username': username, 
        'description': description,
        'image': profile_pic
    }

    return render(request, 'settings/edit.html', context)


class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_reset_done') 


@check_ban
@login_required(login_url='/authentication/login/')
def password_reset_done(request):
    return render(request, 'settings/password_reset_done.html')


@login_required(login_url='/authentication/login/')
def logout(request):
    django_logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("login")