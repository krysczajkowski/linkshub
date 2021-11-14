from django.db.models.fields import NullBooleanField
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.views import View
from django.contrib import messages
import re
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator

from .models import Theme, UserTheme, BackgroundTheme, CustomBackgroundTheme, ButtonTheme, CustomButtonTheme
from account.decorators import check_ban
from dashboard.utils import get_membership
from dashboard.decorators import active_membership
from .forms import BackgroundImageForm
from account.utils import validate_image


# Appearance page
@check_ban
@login_required(login_url='/authentication/login/')
def appearance(request):
    # Get membership status
    membership = get_membership(request.user)

    # Get background themes
    bg_color_themes = BackgroundTheme.objects.filter(type='color')
    bg_gradient_themes = BackgroundTheme.objects.filter(type='gradient')

    # Get free background themes if user has no active membership
    if not membership:
        bg_gradient_themes = bg_gradient_themes.filter(is_premium=0)

    button_color_themes = ButtonTheme.objects.all()

    theme_data = UserTheme.objects.get(user=request.user)

    btn_transparent = False
    if theme_data.button_fill == 'transparent':
        btn_transparent = True


    # Get linkshub label
    linkshub_label = theme_data.linkshub_label

    # Get background theme
    bg_theme_name = theme_data.background_theme

    # Set background color input values
    if not bg_theme_name:
        bg_data = theme_data.custom_background_theme

        bg_font_color = bg_data.font_color

        if bg_data.background_color:
            # Cut first 18 elements cuz it's: background-color: 
            bg_bg_color = bg_data.background_color[18:]
            bg_img_url = "/media/other/camera.png"
        else:
            bg_bg_color = '#ffffff'
            bg_img_url = "/media/" + str(bg_data.background_image) 
            
    else:
        bg_img_url = "/media/other/camera.png"
        bg_bg_color = '#ffffff'
        bg_font_color = '#ffffff'

    # Get button theme
    btn_theme_name = UserTheme.objects.get(user=request.user).button_theme

    # Set button color input values
    if btn_theme_name:
        # Normal button theme
        btn_bg_color = '#ffffff'
        btn_font_color = '#ffffff'

    else:
        # Custom background theme
        btn_data = UserTheme.objects.get(user=request.user).custom_button_theme

        btn_bg_color = btn_data.background_color
        btn_font_color = btn_data.font_color

    context = {
        'bg_color_themes': bg_color_themes,
        'bg_gradient_themes': bg_gradient_themes,
        'button_color_themes': button_color_themes,
        'btn_transparent': btn_transparent,
        'membership': membership,
        'bg_img_url': bg_img_url,
        'bg_bg_color': bg_bg_color,
        'bg_font_color': bg_font_color,
        'btn_bg_color': btn_bg_color,
        'btn_font_color': btn_font_color,
        'linkshub_label': linkshub_label,
        'username': request.user.username
    }

    return render(request, 'appearance/background.html', context)

# Get logged in user's username
class get_user_username(View):
    def post(self, request):

        try:
            username = request.user.username
            return JsonResponse({'username': username})
        except:
            return JsonResponse({'error': 'Error: unauthorized operation.'}, status=409)
 

# Choose background theme
class choose_background_theme(View):
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


# Choose custom background color
class custom_bg_color(View):
    def post(self, request):
        # Check membership
        membership = get_membership(request.user)
        if membership != 1:
            return JsonResponse({'error': 'no-premium'})
            
        data = json.loads(request.body)
        background_color = data['bg_color']

        bg_match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', background_color)

        if bg_match:
            try:
                custom_background_theme, created = CustomBackgroundTheme.objects.get_or_create(user=request.user)

                custom_background_theme.background_color = f'background-color: {background_color}'
                custom_background_theme.background_image = None
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



# Choose custom background image
class custom_bg_image(View):
    def post(self, request):
        # Check membership
        membership = get_membership(request.user)
        if membership != 1:
            return JsonResponse({'error': 'no-premium'})
            
        image = request.FILES.get('background_image')

        # Validate image
        validate_image_output = validate_image(image, True, '')

        if validate_image_output['everything_ok']:
            print('wszystko kox')
            try:
                custom_background_theme, created = CustomBackgroundTheme.objects.get_or_create(user=request.user)

                custom_background_theme.background_image = image
                custom_background_theme.background_color = ''
                custom_background_theme.save()

                user_theme = UserTheme.objects.get(user=request.user)
                user_theme.custom_background_theme = custom_background_theme
                user_theme.background_theme = None 
                user_theme.save()
                
            except:
                return JsonResponse({'error': 'Error: unauthorized operation.'}, status=409)

            return JsonResponse({'success': True})
        else:
            print(validate_image_output['error_msg'])
            return JsonResponse({'error': 'Error: unauthorized operation.'}, status=409)


# Choose custom background font color
class custom_bg_font_color(View):
    def post(self, request):
        # Check membership
        membership = get_membership(request.user)
        if membership != 1:
            return JsonResponse({'error': 'no-premium'})
            
        data = json.loads(request.body)
        font_color = data['font_color']

        font_match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', font_color)

        if font_match:
            try:
                custom_background_theme, created = CustomBackgroundTheme.objects.get_or_create(user=request.user)

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


# Custom button background color
class custom_button_bg_color(View):
    def post(self, request):
        # Check membership
        membership = get_membership(request.user)
        if membership != 1:
            return JsonResponse({'error': 'no-premium'})

        data = json.loads(request.body)
        background_color = data['bg_color']

        bg_match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', background_color)

        if bg_match:
            try:
                custom_button_theme, created = CustomButtonTheme.objects.get_or_create(user=request.user)

                custom_button_theme.background_color = background_color
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

# Custom button font color
class custom_button_font_color(View):
    def post(self, request):
        # Check membership
        membership = get_membership(request.user)
        if membership != 1:
            return JsonResponse({'error': 'no-premium'})

        data = json.loads(request.body)
        font_color = data['font_color']

        font_match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', font_color)

        if font_match:
            try:
                custom_button_theme, created = CustomButtonTheme.objects.get_or_create(user=request.user)

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

# Choose button theme
class choose_button_theme(View):
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

# Choose button fill
class button_fill(View):
    def post(self, request):
        data = json.loads(request.body)
        transparent = data['transparent']
        filled = data['filled']

        try:
            if transparent:
                user_theme = UserTheme.objects.get(user=request.user)
                user_theme.button_fill = 'transparent'
                user_theme.save()
            else:
                user_theme = UserTheme.objects.get(user=request.user)
                user_theme.button_fill = 'filled'
                user_theme.save()

        except:
            return JsonResponse({'error': 'Error: unauthorized operation.'}, status=409)

        return JsonResponse({'success': True})


# Choose link outline
class choose_outline(View):
    def post(self, request):
        # Check membership
        membership = get_membership(request.user)
        if membership != 1:
            return JsonResponse({'error': 'no-premium'})

        data = json.loads(request.body)
        outline = data['outline']

        acceptable_outlines = ['outline-sharp', 'outline-normal', 
        'outline-rounded']

        if outline in acceptable_outlines:
            try:
                user_theme = UserTheme.objects.get(user=request.user)
                user_theme.button_outline = outline
                user_theme.save()

            except:
                return JsonResponse({'error': 'Error: unauthorized operation.'}, status=409)
        else:
            return JsonResponse({'error': 'Error: unauthorized operation.'}, status=409)

        return JsonResponse({'success': True})


# Choose link shadow
class choose_shadow(View):
    def post(self, request):
        # Check membership
        membership = get_membership(request.user)
        if membership != 1:
            return JsonResponse({'error': 'no-premium'})

        data = json.loads(request.body)
        shadow = data['shadow']

        acceptable_shadows = ['shadow-none', 'shadow-soft', 'shadow-normal', 'shadow-hard']

        if shadow in acceptable_shadows:
            try:
                user_theme = UserTheme.objects.get(user=request.user)
                user_theme.button_shadow = shadow
                user_theme.save()

            except:
                return JsonResponse({'error': 'Error: unauthorized operation.'}, status=409)
        else:
            return JsonResponse({'error': 'Error: unauthorized operation.'}, status=409)

        return JsonResponse({'success': True})


# Decide if show linkshub logo
class display_logo(View):
    def post(self, request):
        # Check membership
        membership = get_membership(request.user)
        if membership != 1:
            return JsonResponse({'error': 'no-premium'})

        data = json.loads(request.body)
        display_logo = bool(data['display_logo'])

        user_theme = UserTheme.objects.get(user=request.user)
        user_theme.linkshub_label = display_logo
        user_theme.save()

        return JsonResponse({'success': True})