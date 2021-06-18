from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


from account.models import Profile

# Create your forms here.

class EditForm(forms.ModelForm):
    image = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.jpg, .png', 'required': False}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'required': False}))

    class Meta:
        model = Profile 
        fields = ('image', 'description')


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'Current Password'}), label="")
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'New Password'}), label="")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'Repeat New Password'}), label="")

    class Meta:
        model = User 
        fields = ('old_password', 'new_password1', 'new_password2')