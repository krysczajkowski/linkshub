from django.urls import path

from . import views

urlpatterns = [
    path('link_click', views.link_click.as_view(), name='link_click'),
    path('premium_link_click', views.premium_link_click.as_view(), name='premium_link_click'),
    path('platform_click', views.platform_click.as_view(), name='platform_click'),
    path('', views.dashboard, name='dashboard'),
    path('dashboard_main_chart', views.dashboard_main_chart, name='dashboard_main_chart'),
    path('country_table', views.country_table, name='country_table'),
    path('dashboard_summary', views.dashboard_summary, name='dashboard_summary'),
    path('city_table', views.city_table, name='city_table'),
    path('device_chart', views.device_chart, name='device_chart'),
    path('links', views.links_advanced, name='links_advanced'),
    path('links_advanced_charts', views.links_advanced_charts, name='links_advanced_charts'),
    path('platforms', views.platforms_advanced, name='platforms_advanced'),
    path('platforms_advanced_charts', views.platforms_advanced_charts, name='platforms_advanced_charts'),
    path('premium_links', views.premium_links_advanced, name='premium_links_advanced'),
    path('register_visitor', views.register_visitor.as_view(), name='register_visitor'),
]
