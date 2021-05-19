from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from .models import UserPlatform, Platform

# Create your views here.
@login_required(login_url='/authentication/login/')
def profile(request):
    context = {
        'profile': request.user
    }

    return render(request, 'account/profile.html', context)


@login_required(login_url='/authentication/login/')
def platforms(request):
    # Lista platform użytkownika
    platforms = Platform.objects.all()

    # Tworzenie każdej z platform (jeśli nie istenieje)
    for platform in platforms:
        if platform.is_active:
            try:
                # Aktualizuje link platformy
                user_platform = UserPlatform.objects.get(user=request.user, platform=platform.name)

                if user_platform.platform_url != platform.link:
                    user_platform.platform_url = platform.link
                    user_platform.save()

            #except user_platform.DoesNotExist:
            except:
                # Tworze platformę
                UserPlatform.objects.create(
                    user=request.user,
                    platform = platform.name,
                    platform_url = platform.link
                )


        # Usuwamy starą platformę
        else:
            try:
                unactive_platform = UserPlatform.objects.filter(user=request.user, platform=platform.name)
                unactive_platform.delete()
            except:
                pass


    # Aktywne platformy
    active_platforms = Platform.objects.filter(is_active=True)

    # Świerza lista platform użytkownika
    user_platforms = UserPlatform.objects.filter(user=request.user)

    # Zmienne pod błędy
    error_msg = None
    error_msg_platform = None

    # Formularz przeslany
    if request.method == 'POST':
        # Walidator do url
        validator = URLValidator()

        form_data = request.POST

        # Walidacja każdej platformy
        for platform in active_platforms:
            # Flaga
            everything_ok = 1

            # Walidacja długości username
            platform_username = str(form_data[platform.name]).strip()
            if len(platform_username) > 220:
                everything_ok = 0
                error_msg_platform = f'{platform.name}'
                error_msg = f"Your {platform.name} username is too long."

            # Walidacja poprawności linku
            try:
                validator(f"{platform.link}{platform_username}")
            except ValidationError as exception:
                everything_ok = 0

                error_msg_platform = f'{platform.name}'
                error_msg = f'Link: "{platform.link}{platform_username}" is invalid'

            # Update platformy
            if everything_ok == 1:
                UserPlatformInstance = UserPlatform.objects.get(user=request.user, platform=platform.name)

                UserPlatformInstance.username = platform_username
                UserPlatformInstance.save()

    context = {
        'platforms': user_platforms,
        'error_msg_platform': error_msg_platform,
        'error_msg': error_msg
    }
    return render(request, 'account/platforms.html', context)
