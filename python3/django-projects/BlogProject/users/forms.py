from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import CustomUser


class UserSignUpForm(UserCreationForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 5, 'rows': 5}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'description']
        # widgets = {
        #     'description': forms.Textarea(attrs={'rows': 3})
        # }
