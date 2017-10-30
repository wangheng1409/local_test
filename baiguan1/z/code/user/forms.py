from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext as _

from .models import *

class CMUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CMUser
        # widgets = {
        #     'tagline': forms.Textarea(attrs = {'cols': 80, 'rows': 10}),
        #     'tagline_cn': forms.Textarea(attrs = {'cols': 80, 'rows': 10}),
        # }

class CMUserCreationForm(UserCreationForm):
    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            CMUser._default_manager.get(username=username)
        except CMUser.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    class Meta(UserCreationForm.Meta):
        model = CMUser