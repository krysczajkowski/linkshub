from django import forms
from account.models import Profile
# Create your forms here.

class EditForm(forms.ModelForm):
    image = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.jpg, .png', 'required': False}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'required': False}))

    class Meta:
        model = Profile 
        fields = ('image', 'description')
