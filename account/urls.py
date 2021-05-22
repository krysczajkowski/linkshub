from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('platforms', views.platforms, name='platforms'),
    path('links', views.links, name='links'),
    path('links/add', views.add_link, name='add_link'),
    path('links/activate', csrf_exempt(views.activate_link.as_view()), name='activate_link')
]
