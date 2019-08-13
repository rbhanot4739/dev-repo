from django.forms import inlineformset_factory
from django.forms.models import ModelForm
from .models import FamilyMember


class MemeberForm(ModelForm):

    class Meta:
        model = FamilyMember
        fields = ('name', 'age', 'job', 'parent')