from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('authentication/', include('authentication.urls')),
    path('profile/', include('account.urls')),
    path('settings/', include('settings.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('premium/', include('premium.urls')),
    path('set-up-account/', include('setUpAccount.urls')),
    path('s/', include('sitepolicy.urls')),
    path('<slug:username>', views.profile),
    path('user_banned/', views.user_banned, name='user_banned'),
    path('you_are_banned/', views.you_are_banned, name='you_are_banned'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
