from django import forms

from django.forms import modelformset_factory, inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import MemeberForm
from .models import FamilyMember

# Create your views here.


def create_family_member(request, pk):
    member = FamilyMember.objects.get(pk=pk)

    form = MemeberForm(instance=member)
    if request.POST:
        form = MemeberForm(request.POST or None, instance=member)
        if form.is_valid():
            form.save()
            return redirect("update-member", pk=pk)
    else:
        return render(request, "family/add_member.html", {"form": form})


def add_child(request):
    member = FamilyMember.objects.get(name="Tom")
    child_formset_factory = inlineformset_factory(FamilyMember, FamilyMember, fields=('parent', ))
    # if request.POST:

    formset = child_formset_factory(instance=member)
    return render(request, "family/add_child.html", {"formset": formset})