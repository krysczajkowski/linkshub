from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', views.profile_preview, name='profile_preview'),
    path('appearance/', include('appearance.urls')),
    path('platforms', views.platforms, name='platforms'),
    path('links/', views.links, name='links'),
    path('links/add', views.add_link, name='add_link'),
    path('links/activate', views.activate_link.as_view(), name='activate_link'),
    path('links/delete', views.delete_link.as_view(), name='delete_link'),
    path('links/change_positions', views.change_positions.as_view(), name='change_positions'),
    path('links/edit/<str:link_type>/<int:link_id>', views.edit_link, name='edit_link'),
    path('premium_links/', views.premium_links, name='premium_links'),
    path('premium_links/check_password', views.premium_links_check_password.as_view(), name='premium_links_check_password'),
    path('get_user_theme', views.get_user_theme.as_view(), name='get_user_theme'),
    path('premium_links/add', views.add_premium_link, name='add_premium_link')
]
