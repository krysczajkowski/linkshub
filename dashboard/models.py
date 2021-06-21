from django.db import models
from django.contrib.auth.models import User

from account.models import CustomLink, UserPlatform

# Create your models here.
class ProfileView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    ip_address = models.GenericIPAddressField()


class LinkClick(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    link = models.ForeignKey(CustomLink, on_delete=models.CASCADE, blank=True, null=True)

class PlatformClick(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    platform = models.ForeignKey(UserPlatform, on_delete=models.CASCADE, blank=True, null=True)