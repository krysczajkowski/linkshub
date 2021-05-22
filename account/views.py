from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.contrib import messages
import imghdr


from .models import UserPlatform, Platform, CustomLink

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
            platform_username = str(form_data[platform.name]).replace(" ", "")
            if len(platform_username) > 120:
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


@login_required(login_url='/authentication/login/')
def links(request):
    links = CustomLink.objects.filter(user=request.user).order_by('-id')

    links_count = links.count()

    context = {
    'links': links,
    'links_count': links_count
    }

    return render(request, 'account/links.html', context)

@login_required(login_url='/authentication/login/')
def add_link(request):
    if request.method == 'POST':
        everything_ok = True

        title = request.POST.get('title')
        description = request.POST.get('description')
        url = request.POST.get('url')
        image = request.FILES.get('image', False)

        if len(title) < 1 or len(title) > 70:
            everything_ok = False 
            error_msg = 'Title length must be between 1 and 70 characters.'

        if len(description) > 150:
            everything_ok = False 
            error_msg = 'Description length can not be over 150 characters.'
        
        validator = URLValidator()
        try:
            validator(url)
        except ValidationError as exception:
            everything_ok = False
            error_msg = 'Please provide valid URL.'
        
        if image:
            image_extention = imghdr.what(image)
            
            if image_extention is None:
                everything_ok = False
                error_msg = 'Please provide a valid image.'


        if everything_ok:
            if image:
                link = CustomLink.objects.create(user=request.user, title=title, description=description, url=url, image=image)
            else:
                link = CustomLink.objects.create(user=request.user, title=title, description=description, url=url)

            messages.success(request, 'Link added successfully.')
            return redirect('links')

        else:
            messages.error(request, error_msg)

    return render(request, 'account/add_link.html')


class activate_link(View):
    def post(self, request):
        data = json.loads(request.body)
        link_id = data['link_id']
        is_active = data['is_active']

        try:
            link = CustomLink.objects.get(id=link_id, user=request.user)
            link.is_active = is_active 
            link.save()
        except:
            return JsonResponse({'error': 'Error: unauthorized operation.'}, status=409)

        return JsonResponse({'success': True})