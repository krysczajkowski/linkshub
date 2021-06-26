from django import forms

from .models import CustomLink

# Create your forms here.

class CustomLinkForm(forms.ModelForm):
    class Meta:
        model = CustomLink 
        fields = ('title', 'description', 'url', 'image', 'animation')