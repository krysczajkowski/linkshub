from django.urls import path
from premium import views

urlpatterns = [
    path('join', views.join, name='join'),
    path('success', views.success, name='success'),
    path('cancel', views.cancel, name='cancel'),
    path('updateaccounts', views.updateaccounts, name='updateaccounts'),
    path('start_free_trial', views.start_free_trial.as_view(), name='start_free_trial')
]