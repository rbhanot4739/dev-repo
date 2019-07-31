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
    url(r'password_reset/$', password_reset, {'template_name': "users/password_reset_form.html"},
        name='password_reset'),
    url(r'password_reset/done/$', password_reset_done, {'template_name': "users/password_reset_email.html"},
        name='password_reset_done'),
    url(r'reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm, {'template_name': "users/password_reset_confirm.html"},
        name='password_reset_confirm'),
    url(r'reset/done/$', password_reset_complete, {'template_name': 'users/password_reset_complete.html'},
        name='password_reset_complete')
]
