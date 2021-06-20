from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),
    path('profile/', include('account.urls')),
    path('settings/', include('settings.urls')),
    path('<slug:username>', views.profile)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
