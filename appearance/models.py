from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Theme(models.Model):
    name = models.CharField(max_length=100)
    bg_class_name = models.CharField(max_length=100)
    link_class_name = models.CharField(max_length=100)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class BackgroundTheme(models.Model):
    BG_OPTIONS = [
    ('color', 'color'),
    ('gradient', 'gradient'),
    ('moving_gradient', 'moving_gradient'),
    ]

    name = models.CharField(max_length=100)
    background_color = models.CharField(max_length=100, blank=True)
    font_color = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=100, choices=BG_OPTIONS, blank=True)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class CustomBackgroundTheme(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    background_color = models.CharField(max_length=400)
    background_image = models.ImageField(upload_to='background_image', null=True, blank=True)
    font_color = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.user.username}'


class ButtonTheme(models.Model):
    name = models.CharField(max_length=100)
    background_color = models.CharField(max_length=100, blank=True)
    font_color = models.CharField(max_length=100, blank=True)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class CustomButtonTheme(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    background_color = models.CharField(max_length=100)
    font_color = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.user.username}'

class UserTheme(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    background_theme = models.ForeignKey(BackgroundTheme, on_delete=models.CASCADE, null=True, blank=True)
    custom_background_theme = models.ForeignKey(CustomBackgroundTheme, on_delete=models.CASCADE, null=True, blank=True)
    button_theme = models.ForeignKey(ButtonTheme, on_delete=models.CASCADE, null=True, blank=True)
    custom_button_theme = models.ForeignKey(CustomButtonTheme, on_delete=models.CASCADE, null=True, blank=True)
    button_fill = models.CharField(max_length=120, blank=True)
    button_outline = models.CharField(max_length=120, blank=True)
    button_shadow = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return f'{self.user.username}'


