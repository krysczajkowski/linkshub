from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name= models.CharField(max_length=40, blank=True)
    image = models.ImageField(upload_to='profile_pic', null=True, blank=True)
    description = models.CharField(max_length=300, blank=True, default='')
    premium_links_password = models.CharField(max_length=100, null=True, blank=True)

class BannedUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

class UserPlatform(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=220, null=True, blank=True)
    platform = models.CharField(max_length=220)
    platform_url = models.URLField(max_length=300, null=True, blank=True)

    def __str__(self):
        return f'{self.user} | {self.platform}'


class Platform(models.Model):
    name = models.CharField(max_length=220, null=True, blank=True)
    link = models.URLField(max_length=220, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class LinkAnimation(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name


class CustomLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=220)
    description = models.CharField(max_length=220, blank=True)
    url = models.URLField(max_length=300)
    image = models.ImageField(upload_to='link_img', blank=True, null=True)
    animation = models.ForeignKey(LinkAnimation, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    position = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.title


class PremiumCustomLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=220)
    description = models.CharField(max_length=220, blank=True)
    url = models.URLField(max_length=300)
    image = models.ImageField(upload_to='premium_link_img', blank=True, null=True)
    animation = models.ForeignKey(LinkAnimation, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    position = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.title