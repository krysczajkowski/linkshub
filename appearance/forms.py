from django import forms

from .models import CustomBackgroundTheme

# Create your forms here.

class BackgroundImageForm(forms.ModelForm):
    class Meta:
        model = CustomBackgroundTheme 
        fields = ('background_image',)
