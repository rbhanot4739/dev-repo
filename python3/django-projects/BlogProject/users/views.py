from django.contrib import messages
from django.shortcuts import redirect, render
from .models import CustomUser
from .forms import UserSignUpForm, UserUpdateForm
from django.contrib.auth.views import (password_reset, password_reset_done, password_reset_confirm,
                                       password_reset_complete)


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


def profile(request, uid):
    user = CustomUser.objects.get(pk=uid)
    if request.POST:
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('post-home')
    else:
        print(user)
        form = UserUpdateForm(instance=user)
        return render(request, "users/profile.html", {'form': form})

