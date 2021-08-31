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
from django.contrib.auth.hashers import check_password
from django.core.mail import EmailMessage
import threading

from .forms import EditForm, PasswordChangingForm, DeleteAccountForm
from account.utils import validate_image
from authentication.utils import username_validation
from account.models import Profile
from account.decorators import check_ban

# Create your views here.
class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


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

# Delete user's account
@login_required(login_url='/authentication/login/')
def delete_account(request):
    if request.method == 'POST':
        form = DeleteAccountForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Check if mail is correct
            if email == request.user.email:
                # Check password
                if check_password(password, request.user.password):
                    # Send email
                    email_body = f'Hi {request.user.username}. Your account was deleted successfully.'

                    email_subject = 'Your account is deleted successfully.'

                    email = EmailMessage(
                        email_subject,
                        email_body,
                        'czajkowski.biznes@gmail.com',
                        [email],
                    )
                    EmailThread(email).start()


                    # Delete user
                    user = User.objects.get(username=request.user.username)
                    user.delete()


                    messages.info(request, 'Account deleted successfully.')
                    return redirect('register')
                else:
                    messages.error(request, 'Sorry, password is incorrect.')
            else:
                messages.error(request, 'Sorry, mail is incorrect.')
        else:
            messages.error(request, 'Form is not valid.')

    return render(request, 'settings/delete_account.html')