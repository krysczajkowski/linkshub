from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('platforms', views.platforms, name='platforms'),
    path('links', views.links, name='links'),
    path('links/add', views.add_link, name='add_link')
]
