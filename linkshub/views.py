from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from account.models import UserPlatform, Platform, CustomLink, Profile, BannedUser
from dashboard.models import ProfileView
from appearance.models import BackgroundTheme, Theme, UserTheme, ButtonTheme
from .utils import get_ip

def profile(request, username):
    # Get user 
    user = get_object_or_404(User, username=username)

    # Check user ban
    try:
        user_ban = BannedUser.objects.get(user=user)
        return redirect('user_banned')
            
    except:
        pass

    # Get visitor's ip
    ip = get_ip(request)

    # Register visitor in database if it doesn't exist
    if not ProfileView.objects.filter(ip_address=ip, user=user).exists():
        new_viewer = ProfileView.objects.create(user=user, ip_address=ip)
        new_viewer.save()

    # Get profile
    profile = Profile.objects.get(user=user)

    # Get basic data
    username = request.user.username
    description = profile.description
    profile_picture = profile.image

    # Get all links
    links = CustomLink.objects.filter(user=user, is_active=1).order_by('position')


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

    # Get all social media platforms
    platforms = UserPlatform.objects.filter(user=user, username__gt='',username__isnull=False)

    context = {
        'user_id': user.id,
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

    return render(request, 'linkshub/profile.html', context)


def user_banned(request):
    return render(request, 'linkshub/user_banned.html')

def you_are_banned(request):
    return render(request, 'linkshub/you_are_banned.html')