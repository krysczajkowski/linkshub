from django.contrib import admin
from .models import UserPlatform, Platform, CustomLink, Profile, BannedUser, LinkAnimation, PremiumCustomLink

admin.site.register(UserPlatform)
admin.site.register(Platform)
admin.site.register(CustomLink)
admin.site.register(Profile)
admin.site.register(BannedUser)
admin.site.register(LinkAnimation)
admin.site.register(PremiumCustomLink)