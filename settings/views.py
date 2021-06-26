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

    profile_pic = profile.image

    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES, instance=profile)
        
        if form.is_valid():
            editedForm = form.save()
            messages.success(request, 'Profile updated.')
        else:
            messages.error(request, 'Profile not updated. Please try again.')
        
        return redirect('/settings/edit')
    else:
        form = EditForm(instance=profile)

    context = {
        'form': form,
        'username': username,
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