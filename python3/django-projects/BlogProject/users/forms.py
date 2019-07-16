from .models import CustomUser
from django.forms import ModelForm


class UserRegiterForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
