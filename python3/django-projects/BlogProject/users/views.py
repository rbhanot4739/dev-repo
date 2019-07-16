from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import UserSignUpForm


# Create your views here.


def register(request):
    form = UserSignUpForm()
    if request.POST:
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created')
            return redirect('login')
    return render(request, "users/register.html", {"form": form})

