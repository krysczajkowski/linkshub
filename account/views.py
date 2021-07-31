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
from django.contrib.auth.hashers import make_password
import hashlib

from requests.api import delete

from .models import UserPlatform, Platform, CustomLink, Profile, LinkAnimation, PremiumCustomLink
from appearance.models import BackgroundTheme, Theme, UserTheme, ButtonTheme
from .utils import validate_link_form
from .decorators import check_ban
from .forms import CustomLinkForm, PremiumLinksChangePassword

# Create your views here.
@check_ban
@login_required(login_url='/authentication/login/')
def profile_preview(request):
    # Get profile
    profile = Profile.objects.get(user=request.user)

    user_id = request.user.id

    # Get basic data
    if profile.name:
        username = profile.name
    else:
        username = request.user.username
        
    description = profile.description
    profile_picture = profile.image

    # Get all links
    links = CustomLink.objects.filter(user=request.user, is_active=1).order_by('position')

    # Get premium links
    if PremiumCustomLink.objects.filter(user=request.user, is_active=1).order_by('position') and profile.premium_links_password:
        display_premium_links_password = True 
    else: 
        display_premium_links_password = False

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
        'user_id': user_id, 
        'username': username,
        'description': description,
        'profile_picture': profile_picture,
        'links': links,
        'display_premium_links_password': display_premium_links_password,
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

# Premium links check password
class premium_links_check_password(View):
    def post(self, request):
        data = json.loads(request.body)
        premium_links_code = data['premium_links_code']

        try:
            correct_code = Profile.objects.get(user=request.user).premium_links_password

            # Check password
            if premium_links_code == correct_code:
                premium_links = PremiumCustomLink.objects.filter(user=request.user, is_active=1).order_by('position')

                premium_links_list = []

                for premium_link in premium_links:
                    temp_dict = {}
                    temp_dict['id'] = premium_link.id
                    temp_dict['title'] = premium_link.title
                    temp_dict['url'] = premium_link.url
                    temp_dict['description'] = premium_link.description
                    temp_dict['animation'] = premium_link.animation.name

                    if premium_link.image:
                        temp_dict['image'] = premium_link.image.url
                    else:
                        temp_dict['image'] = ''


                    premium_links_list.append(temp_dict)

                return JsonResponse({'premium_links': premium_links_list}, safe=False)

            else:
                return JsonResponse({'error_msg': 'PASSWORD IS INVALID'})

        except:
            return JsonResponse({'error': 'Error: unauthorized operation.'}, status=409)


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
    form = CustomLinkForm(initial={'title': '', 'description': '', 'url': ''}) 

    if request.method == 'POST':
        form = CustomLinkForm(request.POST, request.FILES)

        if form.is_valid():
            newLink = form.save(commit=False)
            newLink.user = request.user
            newLink.save()

            messages.success(request, 'Link added successfully.')
            return redirect('links')

        else:
            messages.error(request, 'Something went wrong. Please try again.')

    animations = LinkAnimation.objects.all()


    context = {
        'page_title': 'Add Link',
        'form': form,
    }

    return render(request, 'account/add_link.html', context)


def premium_links(request):
    links = PremiumCustomLink.objects.filter(user=request.user).order_by('position')
    links_count = links.count()

    context = {
        'links': links,
        'links_count': links_count
    }


    profile = Profile.objects.get(user=request.user)

    if not profile.premium_links_password:
        change_pass_form = PremiumLinksChangePassword()

        context['change_pass_form'] = change_pass_form
        context['set_password'] = True 

        if request.method == 'POST':
            change_pass_form = PremiumLinksChangePassword(request.POST, instance=profile)
            password = request.POST['premium_links_password']

            if change_pass_form.is_valid():
                new_password = change_pass_form.save(commit=False)
                # assert password
                # new_password.premium_links_password = make_password(password)
                new_password.save()

                messages.success(request, 'Premium Links code updated.')
                return redirect('premium_links')

    else:
        context['set_password'] = False

    return render(request, 'account/premium_links.html', context)


class get_user_theme(View):
    def post(self, request):
        data = json.loads(request.body)
        user_id = data['user_id']

        # Get user
        try: 
            user = User.objects.get(id=user_id)
        except:
            return JsonResponse({'error': 'Error: unauthorized operation.'}, status=409)

        # Get background theme
        bg_theme_name = UserTheme.objects.get(user=user).background_theme

        if bg_theme_name:
            # Normal background theme
            bg_data = BackgroundTheme.objects.get(name=bg_theme_name)

            bg_bg_color = bg_data.background_color
            bg_font_color = bg_data.font_color
        else:
            # Custom background theme
            bg_data = UserTheme.objects.get(user=user).custom_background_theme

            bg_bg_color = bg_data.background_color
            bg_font_color = bg_data.font_color

        # Get button theme
        btn_theme_name = UserTheme.objects.get(user=user).button_theme

        if btn_theme_name:
            # Normal button theme
            btn_data = ButtonTheme.objects.get(name=btn_theme_name)

            btn_bg_color = btn_data.background_color
            btn_font_color = btn_data.font_color
        else:
            # Custom background theme
            btn_data = UserTheme.objects.get(user=user).custom_button_theme

            btn_bg_color = btn_data.background_color
            btn_font_color = btn_data.font_color

        btn_border_color = btn_bg_color

        # Get advanced button theme
        theme_data = UserTheme.objects.get(user=user)
        if theme_data.button_fill == 'transparent':
            btn_font_color = btn_bg_color
            btn_border_color = btn_bg_color
            btn_bg_color = 'transparent'

        btn_outline = theme_data.button_outline
        btn_shadow = theme_data.button_shadow

        data = {
            'bg_bg_color': bg_bg_color,
            'bg_font_color': bg_font_color,
            'btn_font_color': btn_font_color,
            'btn_bg_color': btn_bg_color,
            'btn_border_color': btn_border_color,
            'btn_outline': btn_outline,
            'btn_shadow': btn_shadow
        }

        return JsonResponse({'data': data})


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

    form = CustomLinkForm(instance=link)

    animations = LinkAnimation.objects.all()

    link_animation = link.animation

    context = {
        'page_title': 'Edit Link',
        'delete_existing_image_checkbox': link.image, 
        'form': form
    }

    if request.method == 'POST':
        form = CustomLinkForm(request.POST, request.FILES, instance=link)

        if form.is_valid():
            form.save()

            messages.success(request, 'Link edited successfully.')
            return redirect('links')

        else:
            messages.error(request, 'Something went wrong. Please try again.')

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
