from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserRegiterForm


# Create your views here.


def register(request):
    form = UserRegiterForm()
    if request.POST:
        form = UserRegiterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created')
            return HttpResponse("Valid Form")
    return render(request, "users/create_user.html", {"form": form})


def login(request):
    pass
