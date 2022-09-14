from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from account.decorators import check_ban
from settings.forms import EditForm
from account.models import Profile

@check_ban
@login_required(login_url='/authentication/login/')
def profilePhoto(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            editedForm = form.save()
            result = redirect('platforms')

            # Set up platforms cookie
            result.set_cookie('set-up-platforms', True)

            return result
        else:
            messages.error(request, 'Profile not updated. Please try again.')

    else:
        form = EditForm(instance=profile)

    context = {
        'form': form,
    }

    response = render(request, 'setUpAccount/profile-photo.html', context)

    # Delete the 'set-up-account' cookie
    if 'set-up-account' in request.COOKIES.keys():
        response.delete_cookie('set-up-account')

    return response
