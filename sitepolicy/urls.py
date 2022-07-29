from django.urls import path 
from sitepolicy import views

urlpatterns = [
    path('terms', views.terms, name='terms'),
    path('privacy-policy', views.privacy_policy, name='privacy-policy'),
    path('cookie-policy', views.cookie_policy, name='cookie-policy')
]