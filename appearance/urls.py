from django.urls import path, include

from . import views

urlpatterns = [
    path('background', views.appearance, name='appearance'),
    path('background/choose', views.choose_background.as_view(), name='choose_background'),
    path('background/custom/choose', views.choose_custom_background.as_view(), name='choose_custom_background'),
    path('button/choose', views.choose_button.as_view(), name='choose_button'),
    path('button/custom/choose', views.choose_custom_button.as_view(), name='choose_custom_button'),
]
