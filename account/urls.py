from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('appearance/', include('appearance.urls')),
    path('platforms', views.platforms, name='platforms'),
    path('links/', views.links, name='links'),
    path('links/add', views.add_link, name='add_link'),
    path('links/activate', views.activate_link.as_view(), name='activate_link'),
    path('links/delete', views.delete_link.as_view(), name='delete_link'),
    path('links/edit/<int:link_id>', views.edit_link, name='edit_link'),
]
