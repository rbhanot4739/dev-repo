from django.contrib import messages
from django.shortcuts import redirect, render
from .models import CustomUser
from .forms import UserSignUpForm, UserUpdateForm

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
        userobj = CustomUser.objects.get(pk=uid)
        if request.POST:
                form = UserUpdateForm(request.POST, instance=userobj)
                if form.is_valid():
                        form.save()
                        redirect('post-home')
        else:
                form = UserUpdateForm(request.POST, instance=userobj)
                return render(request, "users/profile.html", {'form': form})