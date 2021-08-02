from django.contrib import admin
from .models import ProfileView, LinkClick, PlatformClick, PremiumLinkClick
# Register your models here.

admin.site.register(ProfileView)
admin.site.register(LinkClick)
admin.site.register(PlatformClick)
admin.site.register(PremiumLinkClick)