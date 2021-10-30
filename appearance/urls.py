from django.urls import path, include

from . import views

urlpatterns = [
    path('background', views.appearance, name='appearance'),
    path('background/choose', views.choose_background_theme.as_view(), name='choose_background'),
    path('button/choose', views.choose_button_theme.as_view(), name='choose_button'),
    path('button/fill', views.button_fill.as_view(), name='button_fill'),
    path('button/outline', views.choose_outline.as_view(), name='choose_outline'),
    path('button/shadow', views.choose_shadow.as_view(), name='choose_shadow'),
    path('get_username', views.get_user_username.as_view(), name='get_user_username'),
    path('background/bg/color', views.custom_bg_color.as_view(), name='custom_bg_color'),
    path('background/bg/image', views.custom_bg_image.as_view(), name='custom_bg_image'),
    path('background/font/color', views.custom_bg_font_color.as_view(), name='custom_bg_font_color'),
    path('button/bg/color', views.custom_button_bg_color.as_view(), name='custom_button_bg_color'),
    path('button/font/color', views.custom_button_font_color.as_view(), name='custom_button_font_color')
]
