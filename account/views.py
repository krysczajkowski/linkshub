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
from imghdr import tests

from requests.api import delete


from .models import UserPlatform, Platform, CustomLink
from appearance.models import BackgroundTheme, Theme, UserTheme, ButtonTheme
from .utils import validate_link_form

# Create your views here.
@login_required(login_url='/authentication/login/')
def profile(request):
    links = CustomLink.objects.filter(user=request.user, is_active=1)
    bg_theme_name = UserTheme.objects.get(user=request.user).background_theme

    if bg_theme_name:
        bg_data = BackgroundTheme.objects.get(name=bg_theme_name)

        bg_bg_color = bg_data.background_color
        bg_font_color = bg_data.font_color
    else:
        bg_data = UserTheme.objects.get(user=request.user).custom_background_theme

        bg_bg_color = bg_data.background_color
        bg_font_color = bg_data.font_color

    btn_theme_name = UserTheme.objects.get(user=request.user).button_theme

    if btn_theme_name:
        btn_data = ButtonTheme.objects.get(name=btn_theme_name)

        btn_bg_color = btn_data.background_color
        btn_font_color = btn_data.font_color
    else:
        btn_data = UserTheme.objects.get(user=request.user).custom_button_theme

        btn_bg_color = btn_data.background_color
        btn_font_color = btn_data.font_color

    btn_border_color = btn_bg_color

    theme_data = UserTheme.objects.get(user=request.user)
    if theme_data.button_fill == 'transparent':
        btn_font_color = btn_bg_color
        btn_border_color = btn_bg_color
        btn_bg_color = 'transparent'

    

    context = {
        'profile': request.user,
        'links': links,
        'bg_bg_color': bg_bg_color,
        'bg_font_color': bg_font_color,
        'btn_font_color': btn_font_color,
        'btn_bg_color': btn_bg_color,
        'btn_border_color': btn_border_color,
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

        messages.success(request, 'Social media platforms updated successfully.')                


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

        title = request.POST.get('title')
        description = request.POST.get('description')
        url = request.POST.get('url')
        image = request.FILES.get('image', False)

        data = validate_link_form(title, description, url, image)

        everything_ok = data['everything_ok']
        error_msg = data['error_msg']

        if everything_ok:
            if image:
                link = CustomLink.objects.create(user=request.user, title=title, description=description, url=url, image=image)
            else:
                link = CustomLink.objects.create(user=request.user, title=title, description=description, url=url)

            messages.success(request, 'Link added successfully.')
            return redirect('links')

        else:
            messages.error(request, error_msg)

    context = {
        'page_title': 'Add Link'
    }

    return render(request, 'account/add_link.html', context)


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


class delete_link(View):
    def post(self, request):
        data = json.loads(request.body)
        link_id = data['link_id']

        try:
            link = CustomLink.objects.get(id=link_id, user=request.user)
            link.delete()
        except:
            return JsonResponse({'error': 'Error: unauthorized operation.'}, status=409)


        messages.success(request, 'Link deleted successfully.')
        return JsonResponse({'success': True})


@login_required(login_url='/authentication/login/')
def edit_link(request, link_id):
    try:
        link = CustomLink.objects.get(id=link_id, user=request.user)
    except:
        return redirect('profile')

    context = {
        'page_title': 'Edit Link',
        'delete_existing_image_checkbox': True, 
        'title': link.title,
        'description': link.description,
        'url': link.url,
        'image': link.image
    }

    if request.method == 'POST':
        everything_ok = True

        title = request.POST.get('title')
        description = request.POST.get('description')
        url = request.POST.get('url')
        image = request.FILES.get('image', False)
        delete_existing_thumbnail = request.POST.get('delete_existing_thumbnail', False)

        data = validate_link_form(title, description, url, image)

        everything_ok = data['everything_ok']
        error_msg = data['error_msg']

        if everything_ok:
            link.title = title 
            link.description = description 
            link.url = url 

            if image:
                link.image = image
                
            else:
                if delete_existing_thumbnail:
                    link.image = None 

            link.save()
            messages.success(request, 'Link updated successfully.')
            return redirect('links')

        else:
            messages.error(request, error_msg)


    print(context)
    return render(request, 'account/add_link.html', context)

@login_required(login_url='/authentication/login/')
def themes(request):
    return render(request, 'account/themes.html')