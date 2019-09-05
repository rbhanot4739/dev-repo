from django.urls import path, re_path
from .views import activate_account, profile, register
from django.contrib.auth.views import (LoginView, LogoutView, PasswordResetView, PasswordResetDoneView,
                                       PasswordResetConfirmView, PasswordResetCompleteView)

urlpatterns = [
    path('register/', register, name='register-user'),
    re_path(r'profile/(?P<uid>\d+)/$', profile, name='user-profile'),
    path('login/', LoginView.as_view(template_name="users/login.html"), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    # url(r'password_reset/$', password_reset, {'template_name': "users/password_reset_form.html"},
    #     name='password_reset'),
    # url(r'password_reset/done/$', password_reset_done, {'template_name': "users/password_reset_email.html"},
    #     name='password_reset_done'),
    # url(r'reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     password_reset_confirm, {'template_name': "users/password_reset_confirm.html"},
    #     name='password_reset_confirm'),
    # url(r'reset/done/$', password_reset_complete, {'template_name': 'users/password_reset_complete.html'},
    #     name='password_reset_complete'),
    # url(r'activate/(?P<uid>[\w]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate_account,
    #     name='account-activate')
]
