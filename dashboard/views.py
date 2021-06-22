from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import json
from django.contrib.auth.models import User

from account.models import CustomLink, UserPlatform
from dashboard.models import LinkClick, PlatformClick
from account.decorators import check_ban

# Create your views here.
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