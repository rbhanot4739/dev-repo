from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from .models import User
from .forms import UserSignUpForm, UserUpdateForm
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

token_generator = PasswordResetTokenGenerator()


# Create your views here.

def register(request):
    form = UserSignUpForm()
    if request.POST:
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.is_active = False
            user.is_active = True
            user.save()
            # mail_message = render_to_string("users/registration_email.html",
            #                                 {'user': urlsafe_base64_encode(force_bytes(user.id)),
            #                                  'token': token_generator.make_token(user),
            #                                  })
            # email = EmailMessage('Activate your account', mail_message, to=[user.email])
            # email.content_subtype = "html"
            # email.send()
            messages.success(request, 'Please check your email for activation.')
            return redirect('post-home')
    return render(request, "users/register.html", {"form": form})


def profile(request, uid):
    user = User.objects.get(pk=uid)
    if request.POST:
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('post-home')
    else:
        print(user)
        form = UserUpdateForm(instance=user)
        return render(request, "users/profile.html", {'form': form})


def activate_account(request, uid, token):
    uid = force_text(urlsafe_base64_decode(uid))
    user = User.objects.get(pk=uid)
    if user and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Account Activated Successfully')
        return redirect('post-home')
    else:
        return HttpResponseForbidden()
