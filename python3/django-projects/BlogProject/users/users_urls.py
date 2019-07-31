from django.conf.urls import url
from django.contrib.auth.views import login, logout

from .views import register, profile
from django.contrib.auth.views import (password_reset, password_reset_done, password_reset_confirm,
                                       password_reset_complete)

urlpatterns = [
    url(r'register/$', register, name='register-user'),
    url(r'profile/(?P<uid>\d+)$', profile, name='user-profile'),
    url(r'login/$', login, {'template_name': "users/login.html"}, name='login'),
    url(r'logout/$', logout, {'next_page': 'login'}, name='logout'),
    url(r'password_reset/$', password_reset, {'template_name': "users/password_reset.html"},
        name='password_reset'),
    url(r'password_reset_done/', password_reset_done, name='password_reset_done'),
    url(r'password_reset_confirm/', password_reset_confirm, name='password_reset_confirm'),
    url(r'password_reset_complete/', password_reset_complete, name='password_reset_complete')
]
