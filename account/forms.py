from django import forms

from .models import CustomLink, PremiumCustomLink, Profile

# Create your forms here.

class CustomLinkForm(forms.ModelForm):
    class Meta:
        model = CustomLink 
        fields = ('title', 'description', 'url', 'image', 'animation', 'display_as_yt_embed')

    def __init__(self, *args, **kwargs):
        super(CustomLinkForm, self).__init__(*args, **kwargs)
        self.fields['animation'].empty_label = None


class CustomPremiumLinkForm(forms.ModelForm):
    class Meta:
        model = PremiumCustomLink 
        fields = ('title', 'description', 'url', 'image', 'animation', 'display_as_yt_embed')

    def __init__(self, *args, **kwargs):
        super(CustomPremiumLinkForm, self).__init__(*args, **kwargs)
        self.fields['animation'].empty_label = None


class PremiumLinksChangePassword(forms.ModelForm):
    class Meta:
        model = Profile 
        fields = ('premium_links_password',)

