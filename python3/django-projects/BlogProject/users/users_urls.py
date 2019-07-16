from django.conf.urls import url
from django.contrib.auth.views import login, logout

from .views import register

urlpatterns = [
    url(r'register/$', register, name='register-user'),
    url(r'login/$', login, {'template_name': "users/login.html"}, name='login'),
    url(r'logout/', logout, {'next_page': 'login'}, name='logout')
]
