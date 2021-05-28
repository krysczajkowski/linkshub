from django.db.models.fields import NullBooleanField
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.views import View
from django.contrib import messages
import re

from .models import Theme, UserTheme, BackgroundTheme, CustomBackgroundTheme, ButtonTheme, CustomButtonTheme

# Create your views here.
@login_required(login_url='/authentication/login/')
def appearance(request):
    bg_color_themes = BackgroundTheme.objects.filter(type='color')
    bg_gradient_themes = BackgroundTheme.objects.filter(type='gradient')

    button_color_themes = ButtonTheme.objects.all()

    context = {
        'bg_color_themes': bg_color_themes,
        'bg_gradient_themes': bg_gradient_themes,
        'button_color_themes': button_color_themes
    }

    return render(request, 'appearance/background.html', context)

class choose_background(View):
    def post(self, request):
        data = json.loads(request.body)
        theme_id = data['theme_id']

        try:
            background_theme = BackgroundTheme.objects.get(id=theme_id)
            user_theme_relationship = UserTheme.objects.get(user=request.user)
            user_theme_relationship.background_theme = background_theme 
            user_theme_relationship.custom_background_theme = None
            user_theme_relationship.save()

        except:
            return JsonResponse({'error': 'Error: unauthorized operation.'}, status=409)

        return JsonResponse({'success': True})

    
class choose_custom_background(View):
    def post(self, request):
        data = json.loads(request.body)
        background_color = data['bg_color']
        font_color = data['font_color']

        bg_match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', background_color)

        font_match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', font_color)

        if bg_match and font_match:
            try:
                custom_background_theme, created = CustomBackgroundTheme.objects.get_or_create(user=request.user)

                custom_background_theme.background_color = f'background-color: {background_color}'
                custom_background_theme.font_color = font_color 
                custom_background_theme.save()

                user_theme = UserTheme.objects.get(user=request.user)
                user_theme.custom_background_theme = custom_background_theme
                user_theme.background_theme = None 
                user_theme.save()
                
            except:
                return JsonResponse({'error': 'Error: unauthorized operation.'}, status=409)
        else:
            return JsonResponse({'error': 'Error: unauthorized operation.'}, status=409)

        return JsonResponse({'success': True})


class choose_button(View):
    def post(self, request):
        data = json.loads(request.body)
        theme_id = data['theme_id']

        try:
            button_theme = ButtonTheme.objects.get(id=theme_id)
            user_theme_relationship = UserTheme.objects.get(user=request.user)
            user_theme_relationship.button_theme = button_theme 
            user_theme_relationship.custom_button_theme = None
            user_theme_relationship.save()

        except:
            return JsonResponse({'error': 'Error: unauthorized operation.'}, status=409)

        return JsonResponse({'success': True})


class choose_custom_button(View):
    def post(self, request):
        data = json.loads(request.body)
        background_color = data['bg_color']
        font_color = data['font_color']

        bg_match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', background_color)

        font_match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', font_color)

        if bg_match and font_match:
            try:
                custom_button_theme, created = CustomButtonTheme.objects.get_or_create(user=request.user)

                custom_button_theme.background_color = background_color
                custom_button_theme.font_color = font_color 
                custom_button_theme.save()

                user_theme = UserTheme.objects.get(user=request.user)
                user_theme.custom_button_theme = custom_button_theme
                user_theme.button_theme = None 
                user_theme.save()
                
            except:
                return JsonResponse({'error': 'Error: unauthorized operation.'}, status=409)
        else:
            return JsonResponse({'error': 'Error: unauthorized operation.'}, status=409)

        return JsonResponse({'success': True})