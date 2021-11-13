from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
import datetime

from account.models import UserPlatform, Platform, CustomLink, Profile, BannedUser, PremiumCustomLink
from dashboard.models import ProfileView
from appearance.models import BackgroundTheme, Theme, UserTheme, ButtonTheme
from dashboard.utils import get_ip, get_location, get_membership
from premium.models import Customer, PremiumFreeTrial

def index(request):
    # Check if user is authenticated
    if request.user.is_authenticated:
        return redirect('/profile/')
    
    return render(request, 'linkshub/index.html')

def profile(request, username):
    # Get user 
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)

    # Get membership
    membership = get_membership(user)

    # Check user ban
    try:
        user_ban = BannedUser.objects.get(user=user)
        return redirect('user_banned')
            
    except:
        pass

    # Get premium links
    if membership:
        if PremiumCustomLink.objects.filter(user=user, is_active=1).order_by('position') and profile.premium_links_password:
            display_premium_links_password = True 
        else: 
            display_premium_links_password = False
    else:
        display_premium_links_password = False

    # Get profile
    profile = Profile.objects.get(user=user)

    # Get basic data
    if profile.name:
        username = profile.name
    else:
        username = user.username

    description = profile.description
    
    if profile.image:
        profile_picture = profile.image.url
    else:
        profile_picture = '/media/profile_pic/defaultProfilePicture.png'

    # Get all links
    links = CustomLink.objects.filter(user=user, is_active=1).order_by('position')

    # Get all social media platforms
    platforms = UserPlatform.objects.filter(user=user, username__gt='',username__isnull=False)

    # Get user theme function is in account/views.py

    context = {
        'user_id': user.id,
        'membership': membership,
        'username': username,
        'description': description,
        'profile_picture': profile_picture,
        'links': links,
        'display_premium_links_password': display_premium_links_password,
        'platforms': platforms,
    }
    return render(request, 'linkshub/profile.html', context)


def user_banned(request):
    return render(request, 'linkshub/user_banned.html')

def you_are_banned(request):
    return render(request, 'linkshub/you_are_banned.html')