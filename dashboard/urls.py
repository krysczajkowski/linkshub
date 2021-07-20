from django.urls import path

from . import views

urlpatterns = [
    path('link_click', views.link_click.as_view(), name='link_click'),
    path('platform_click', views.platform_click.as_view(), name='platform_click'),
    path('', views.dashboard, name='dashboard'),
    path('dashboard_main_chart', views.dashboard_main_chart, name='dashboard_main_chart'),
    path('location_table', views.location_table, name='location_table'),
    path('dashboard_summary', views.dashboard_summary, name='dashboard_summary')
]
