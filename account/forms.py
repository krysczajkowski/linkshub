from django import forms

from .models import CustomLink

# Create your forms here.

class CustomLinkForm(forms.ModelForm):
    class Meta:
        model = CustomLink 
        fields = ('title', 'description', 'url', 'image', 'animation')

    def __init__(self, *args, **kwargs):
        super(CustomLinkForm, self).__init__(*args, **kwargs)
        self.fields['animation'].empty_label = None