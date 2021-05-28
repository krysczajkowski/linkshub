from django.contrib import admin

from .models import Theme, UserTheme, BackgroundTheme, CustomBackgroundTheme, ButtonTheme, CustomButtonTheme

# Register your models here.
admin.site.register(Theme)
admin.site.register(UserTheme)
admin.site.register(BackgroundTheme)
admin.site.register(CustomBackgroundTheme)
admin.site.register(ButtonTheme)
admin.site.register(CustomButtonTheme)