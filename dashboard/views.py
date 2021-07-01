from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import json
from django.contrib.auth.models import User
import datetime

from account.models import CustomLink, UserPlatform
from dashboard.models import LinkClick, PlatformClick, ProfileView
from account.decorators import check_ban

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


def profile_views_summary(request):
    today = datetime.date.today()
    three_months_age = today - datetime.timedelta(days=30*3)

    profile_views = ProfileView.objects.filter(user=request.user, date__gte=three_months_age)

    chart_data = {}

    def get_view_date(view):
        return view.date

    def get_date_views(date):
        views = 0 

        filtered_by_date = profile_views.filter(date=date)

        for item in filtered_by_date:
            views += 1

        return views

    date_list = list(set(map(get_view_date, profile_views)))

    for date in date_list:
        date_as_string = date.strftime('%Y-%m-%d %H')
        chart_data[date_as_string] = get_date_views(date)

    return JsonResponse({'chart_data': chart_data}, safe=False)    

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