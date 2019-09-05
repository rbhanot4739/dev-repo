from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import User


class UserSignUpForm(UserCreationForm):
    # description = forms.CharField(widget=forms.Textarea(attrs={'cols': 3, 'rows': 4}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3})
        }


class UserUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'description', ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'username': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email': forms.TextInput(attrs={'readonly': 'readonly'})
        }
