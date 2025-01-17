from django.db import models
from django.contrib.auth.models import User

from account.models import CustomLink, PremiumCustomLink, UserPlatform

# Create your models here.
class ProfileView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    ip_address = models.GenericIPAddressField()
    country = models.CharField(max_length=70, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True) 
    device = models.CharField(max_length=50, blank=True, null=True) 
    date = models.DateTimeField(auto_now_add=True, blank=True)


class LinkClick(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    link = models.ForeignKey(CustomLink, on_delete=models.CASCADE, blank=True, null=True)
    country = models.CharField(max_length=70, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True) 
    date = models.DateTimeField(auto_now_add=True, blank=True)

class PremiumLinkClick(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    link = models.ForeignKey(PremiumCustomLink, on_delete=models.CASCADE, blank=True, null=True)
    country = models.CharField(max_length=70, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True) 
    date = models.DateTimeField(auto_now_add=True, blank=True)

class PlatformClick(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    platform = models.ForeignKey(UserPlatform, on_delete=models.CASCADE, blank=True, null=True)
    country = models.CharField(max_length=70, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True) 
    date = models.DateTimeField(auto_now_add=True, blank=True)