from django.db import models
from django.contrib.auth.models import User

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

class CustomLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=220)
    description = models.CharField(max_length=220, blank=True)
    url = models.URLField(max_length=300)
    image = models.ImageField(upload_to='link_img', blank=True, null=True)

    def __str__(self):
        return self.title
