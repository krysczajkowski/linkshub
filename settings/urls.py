from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('edit', views.edit, name='edit'),
    path('edit/password', views.PasswordChangeView.as_view(template_name='settings/change_password.html'), name='change_password'),
    path('edit/password/done', views.password_reset_done, name='password_reset_done')
]