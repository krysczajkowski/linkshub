from django.contrib import admin

from .models import Customer, PremiumFreeTrial

# Register your models here.
admin.site.register(Customer)
admin.site.register(PremiumFreeTrial)