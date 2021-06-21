from django.urls import path

from . import views

urlpatterns = [
    path('link_click', views.link_click.as_view(), name='link_click'),
    path('platform_click', views.platform_click.as_view(), name='platform_click'),
]
