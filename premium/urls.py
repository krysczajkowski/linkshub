from django.urls import path
from premium import views

urlpatterns = [
    path('join', views.join, name='join'),
    path('success', views.success, name='success'),
    path('cancel', views.cancel, name='cancel'),
    path('updateaccounts', views.updateaccounts, name='updateaccounts'),
]