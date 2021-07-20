from django import views
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import json
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime
import collections

from account.models import CustomLink, Platform, UserPlatform
from dashboard.models import LinkClick, PlatformClick, ProfileView
from account.decorators import check_ban
from .utils import get_view_date, get_ip, get_location

# Dashboard view
@check_ban
@login_required(login_url='/authentication/login/')
def dashboard(request):
    views_count = ProfileView.objects.filter(user=request.user).count()
    link_clicks = LinkClick.objects.filter(user=request.user).count()
    platform_clicks = PlatformClick.objects.filter(user=request.user).count()

    try:
        lcpr_percent =  link_clicks / views_count * 100
    except ZeroDivisionError:
        lcpr_percent = 0

    context = {
        'views': views_count,
        'link_clicks': link_clicks,
        'platform_clicks': platform_clicks,
        'lcpr': lcpr_percent
    }
    return render(request, 'dashboard/dashboard.html', context)

# Dashboard summary chart 
def dashboard_summary_chart(request):  
    # Time period for the chart
    data = json.loads(request.body)

    try:
        # Time period as a string
        str_sdate = data['sdate'][:10]
        str_edate = data['edate'][:10]

        # Time period as a date 
        sdate = datetime.datetime.strptime(str_sdate, '%Y-%m-%d')
        edate = datetime.datetime.strptime(str_edate, '%Y-%m-%d')

    except (ValueError, NameError) as e:
        return JsonResponse({'error': 'Error: unauthorized operation.'}, status=409)

    # Time delta
    delta = edate - sdate

    try:
        # Data for chart
        profile_views = ProfileView.objects.filter(user=request.user)
        link_clicks = LinkClick.objects.filter(user=request.user)
        platform_clicks = PlatformClick.objects.filter(user=request.user)
    except:
        return JsonResponse({'error': 'Error: unauthorized operation.'}, status=409)

    # Create list for final chart data
    datelist = []
    views_data = [] 
    link_data = []
    platform_data = []

    try:
        # Final dates in the chart
        for i in range(delta.days + 1):
            date = sdate + datetime.timedelta(days=i)
            pretty_date = datetime.datetime.strptime(str(date)[:10],'%Y-%m-%d').date()
            datelist.append(pretty_date)
    except:
        return JsonResponse({'error': 'Error: unauthorized operation.'}, status=409)
    

    # Final views, link and platform data in the chart
    for date in datelist:
        # Get time slots for one date: 21.07.06 00:00:00 - 21.07.06 23:59:59
        date_str = date.strftime('%Y-%m-%d')
        date_end = date_str + ' 23:59:59'

        # Final views, link and platform data in the chart
        views_by_date = profile_views.filter(date__gte=date, date__lte=date_end).count()
        links_by_date = link_clicks.filter(date__gte=date, date__lte=date_end).count()
        platforms_by_date = platform_clicks.filter(date__gte=date, date__lte=date_end).count()

        views_data.append(views_by_date)
        link_data.append(links_by_date)
        platform_data.append(platforms_by_date)

    # Send chart data back to javascript
    return JsonResponse({'datelist': datelist, 'views_data': views_data, 'link_data': link_data, 'platform_data': platform_data}, safe=False)


# Location table
def location_table(request): 
    # Time period for the table
    data = json.loads(request.body)

    try:
        # Time period as a string
        sdate = data['sdate'][:10] + ' 00:00:00'
        edate = data['edate'][:10] + ' 23:59:59'

    except (ValueError, NameError) as e:
        return JsonResponse({'error': 'Error: unauthorized operation.'}, status=409)

    try:
        profile_views = ProfileView.objects.filter(user=request.user, date__gte=sdate, date__lte=edate)
        links_clicks = LinkClick.objects.filter(user=request.user, date__gte=sdate, date__lte=edate)
        platforms_clicks = PlatformClick.objects.filter(user=request.user, date__gte=sdate, date__lte=edate)
    except:
        return JsonResponse({'error': 'Error: unauthorized operation.'}, status=409)
 
    countries = list(set(ProfileView.objects.filter(user=request.user).exclude(country__isnull=True).values_list('country', flat=True)))

    data = []

    for country in countries:
        visitors = profile_views.filter(country=country).count()
        country_links_clicks = links_clicks.filter(country=country).count()
        country_platforms_clicks = platforms_clicks.filter(country=country).count()

        temp_dict = {'country': country, 'visitors': visitors, 'links_clicks': country_links_clicks, 'platforms_clicks': country_platforms_clicks}

        data.append(temp_dict)

    return JsonResponse({'data': data}, safe=False)


# Add link click  
class link_click(View):
    def post(self, request):
        data = json.loads(request.body)
        link_id = data['link_id']
        user_id = data['user_id']

        # Get visitors location
        location_info = get_location(request)
        country = location_info['country']
        city = location_info['city']


        try:
            user = User.objects.get(id=user_id)

            link = CustomLink.objects.get(id=link_id, user=user)
            link_click = LinkClick.objects.create(user=request.user, link=link, country=country, city=city)

        except:
            return JsonResponse({'error': 'Error: unauthorized operation.'}, status=409)

        return JsonResponse({'success': True})


# Add platform click
class platform_click(View):
    def post(self, request):
        data = json.loads(request.body)
        platform_id = data['platform_id']
        user_id = data['user_id']

        # Get visitors location
        location_info = get_location(request)
        country = location_info['country']
        city = location_info['city']

        try:
            user = User.objects.get(id=user_id)

            platform = UserPlatform.objects.get(id=platform_id, user=user)
            platform_click = PlatformClick.objects.create(user=request.user, platform=platform, country=country, city=city)

        except:
            return JsonResponse({'error': 'Error: unauthorized operation.'}, status=409)

        return JsonResponse({'success': True})