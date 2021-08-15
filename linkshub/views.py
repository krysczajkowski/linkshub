from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User

from account.models import UserPlatform, Platform, CustomLink, Profile, BannedUser, PremiumCustomLink
from dashboard.models import ProfileView
from appearance.models import BackgroundTheme, Theme, UserTheme, ButtonTheme
from dashboard.utils import get_ip, get_location
from premium.models import Customer

def profile(request, username):
    # Get user 
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)

    # Get membership status
    try: 
        membership = Customer.objects.get(user=user).membership
    except:
        membership = 0

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


    ip = get_ip(request)
    
    # Get visitors location
    location_info = get_location(request)
    country = location_info['country']
    city = location_info['city']

    # Register visitor in database if it doesn't exist
    # if not ProfileView.objects.filter(ip_address=ip, user=user).exists():

    user_agent = request.META['HTTP_USER_AGENT']

    keywords = ['Mobile','Opera Mini','Android']

    if any(word in user_agent for word in keywords):
        device = 'Mobile'
    else:
        device = 'Desktop'

    new_visitor = ProfileView.objects.create(user=user, ip_address=ip, country=country, city=city, device=device)
    new_visitor.save()

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