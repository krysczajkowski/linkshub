from django.urls import path
from premium import views

from setUpAccount import views

urlpatterns = [
    path('profile-photo', views.profilePhoto, name='set-up-profile-photo'),
]
