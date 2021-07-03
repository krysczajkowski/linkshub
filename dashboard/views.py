from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import json
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime
import collections

from account.models import CustomLink, UserPlatform
from dashboard.models import LinkClick, PlatformClick, ProfileView
from account.decorators import check_ban
from .utils import get_view_date

# Dashboard view
@check_ban
@login_required(login_url='/authentication/login/')
def dashboard(request):
    views_count = ProfileView.objects.filter(user=request.user).count()
    clicks_count = LinkClick.objects.filter(user=request.user).count()

    try:
        cpr_percent =  clicks_count / views_count * 100
    except ZeroDivisionError:
        cpr_percent = 0

    print(ProfileView.objects.filter(user=request.user))

    context = {
        'views': views_count,
        'clicks': clicks_count,
        'cpr': cpr_percent
    }
    return render(request, 'dashboard/dashboard.html', context)

# Load profile views data for chart
def profile_views_summary(request):
    # Get profile views from 3 months ago to today
    today = datetime.date.today()
    three_months_age = today - datetime.timedelta(days=30*3)
    profile_views = ProfileView.objects.filter(user=request.user, date__gte=three_months_age)

    chart_data = {}

    # Get all views in a specific time
    def get_date_views(date):
        # Set time slots
        date_start = date.replace(microsecond=0, second=0, minute=0)
        date_end = date.replace(microsecond=59, second=59, minute=59)

        # Get all views from the time slot
        views_by_date = profile_views.filter(date__gte=date_start, date__lte=date_end).count()

        return views_by_date

    # Get list of dates
    date_list = list(set(map(get_view_date, profile_views)))

    # Create a dictionary with dates and visitations
    for date in date_list:
        date_as_string = date.strftime('%Y-%m-%d %H')
        chart_data[date_as_string] = get_date_views(date)

    # Order char_data by date (ascending)
    order_chart_data = collections.OrderedDict(sorted(chart_data.items()))

    return JsonResponse({'chart_data': order_chart_data}, safe=False)    


# Add link click  
class link_click(View):
    def post(self, request):
        data = json.loads(request.body)
        link_id = data['link_id']
        user_id = data['user_id']

        try:
            user = User.objects.get(id=user_id)

            link = CustomLink.objects.get(id=link_id, user=user)
            link_click = LinkClick.objects.create(user=request.user, link=link)

        except:
            return JsonResponse({'error': 'Error: unauthorized operation.'}, status=409)

        return JsonResponse({'success': True})


# Add platform click
class platform_click(View):
    def post(self, request):
        data = json.loads(request.body)
        platform_id = data['platform_id']
        user_id = data['user_id']

        try:
            user = User.objects.get(id=user_id)

            platform = UserPlatform.objects.get(id=platform_id, user=user)
            platform_click = PlatformClick.objects.create(user=request.user, platform=platform)

        except:
            return JsonResponse({'error': 'Error: unauthorized operation.'}, status=409)

        return JsonResponse({'success': True})