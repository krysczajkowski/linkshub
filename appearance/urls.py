from django.urls import path, include

from . import views

urlpatterns = [
    path('background', views.appearance, name='appearance'),
    path('background/choose', views.choose_background.as_view(), name='choose_background'),
    path('background/custom/choose', views.choose_custom_background.as_view(), name='choose_custom_background')
]
