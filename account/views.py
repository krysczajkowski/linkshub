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


from .models import UserPlatform, Platform, CustomLink, Profile, LinkAnimation
from appearance.models import BackgroundTheme, Theme, UserTheme, ButtonTheme
from .utils import validate_link_form
from .decorators import check_ban

# Create your views here.
@check_ban
@login_required(login_url='/authentication/login/')
def profile_preview(request):
    # Get profile
    profile = Profile.objects.get(user=request.user)

    # Get basic data
    username = request.user.username
    description = profile.description
    profile_picture = profile.image

    # Get all links
    links = CustomLink.objects.filter(user=request.user, is_active=1).order_by('position')


    # Get background theme
    bg_theme_name = UserTheme.objects.get(user=request.user).background_theme

    if bg_theme_name:
        # Normal background theme
        bg_data = BackgroundTheme.objects.get(name=bg_theme_name)

        bg_bg_color = bg_data.background_color
        bg_font_color = bg_data.font_color
    else:
        # Custom background theme
        bg_data = UserTheme.objects.get(user=request.user).custom_background_theme

        bg_bg_color = bg_data.background_color
        bg_font_color = bg_data.font_color

    # Get button theme
    btn_theme_name = UserTheme.objects.get(user=request.user).button_theme

    if btn_theme_name:
        # Normal button theme
        btn_data = ButtonTheme.objects.get(name=btn_theme_name)

        btn_bg_color = btn_data.background_color
        btn_font_color = btn_data.font_color
    else:
        # Custom background theme
        btn_data = UserTheme.objects.get(user=request.user).custom_button_theme

        btn_bg_color = btn_data.background_color
        btn_font_color = btn_data.font_color

    btn_border_color = btn_bg_color

    # Get advanced button theme
    theme_data = UserTheme.objects.get(user=request.user)
    if theme_data.button_fill == 'transparent':
        btn_font_color = btn_bg_color
        btn_border_color = btn_bg_color
        btn_bg_color = 'transparent'

    btn_outline = theme_data.button_outline
    btn_shadow = theme_data.button_shadow

    # Get all social media platforms
    platforms = UserPlatform.objects.filter(user=request.user, username__gt='',username__isnull=False)

    context = {
        'username': username,
        'description': description,
        'profile_picture': profile_picture,
        'links': links,
        'bg_bg_color': bg_bg_color,
        'bg_font_color': bg_font_color,
        'btn_font_color': btn_font_color,
        'btn_bg_color': btn_bg_color,
        'btn_border_color': btn_border_color,
        'platforms': platforms,
        'btn_outline': btn_outline,
        'btn_shadow': btn_shadow
    }

    return render(request, 'account/profile_preview.html', context)


@check_ban
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


@check_ban
@login_required(login_url='/authentication/login/')
def links(request):
    links = CustomLink.objects.filter(user=request.user).order_by('position')

    links_count = links.count()

    context = {
    'links': links,
    'links_count': links_count
    }

    return render(request, 'account/links.html', context)

@check_ban
@login_required(login_url='/authentication/login/')
def add_link(request):
    if request.method == 'POST':

        title = request.POST.get('title')
        description = request.POST.get('description')
        url = request.POST.get('url')
        image = request.FILES.get('image', False)
        animation = request.POST.get('animation')

        data = validate_link_form(title, description, url, image, animation)

        everything_ok = data['everything_ok']
        error_msg = data['error_msg']

        if everything_ok:
            animation = LinkAnimation.objects.get(name=animation)

            if image:
                link = CustomLink.objects.create(user=request.user, title=title, description=description, url=url, image=image, animation=animation)
            else:
                link = CustomLink.objects.create(user=request.user, title=title, description=description, url=url, animation=animation)

            messages.success(request, 'Link added successfully.')
            return redirect('links')

        else:
            messages.error(request, error_msg)

    animations = LinkAnimation.objects.all()


    context = {
        'page_title': 'Add Link',
        'animations': animations
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


@check_ban
@login_required(login_url='/authentication/login/')
def edit_link(request, link_id):
    try:
        link = CustomLink.objects.get(id=link_id, user=request.user)
    except:
        return redirect('profile')


    animations = LinkAnimation.objects.all()

    link_animation = link.animation
    print(link_animation)

    context = {
        'page_title': 'Edit Link',
        'delete_existing_image_checkbox': True, 
        'title': link.title,
        'description': link.description,
        'url': link.url,
        'image': link.image,
        'animations': animations,
        'link_animation': link_animation
    }

    if request.method == 'POST':
        everything_ok = True

        title = request.POST.get('title')
        description = request.POST.get('description')
        url = request.POST.get('url')
        image = request.FILES.get('image', False)
        delete_existing_thumbnail = request.POST.get('delete_existing_thumbnail', False)
        animation = request.POST.get('animation')

        data = validate_link_form(title, description, url, image, animation)

        everything_ok = data['everything_ok']
        error_msg = data['error_msg']

        if everything_ok:
            animation = LinkAnimation.objects.get(name=animation)

            link.title = title 
            link.description = description 
            link.url = url 
            link.animation = animation

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

    return render(request, 'account/add_link.html', context)

@check_ban
@login_required(login_url='/authentication/login/')
def themes(request):
    return render(request, 'account/themes.html')


class change_positions(View):
    def post(self, request):
        data = json.loads(request.body)
        positions = data['positions']
        
        try:
            for id, position in positions:
                link = CustomLink.objects.get(id=id)
                link.position = position 
                link.save()
        except (ValueError, CustomLink.DoesNotExist) as e:
            return JsonResponse({'error': 'Error: unauthorized operation.'}, status=409)
            


        return JsonResponse({'success': True})
