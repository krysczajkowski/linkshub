from django.contrib import admin
from .models import UserPlatform, Platform, CustomLink

admin.site.register(UserPlatform)
admin.site.register(Platform)
admin.site.register(CustomLink)
